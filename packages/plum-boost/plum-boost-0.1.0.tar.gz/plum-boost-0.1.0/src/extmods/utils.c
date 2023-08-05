#include <Python.h>
#include "structmember.h"
#include "fast.h"
#include "utils_docstrings.c"

PyObject *PyErr_ExcessMemoryError;
PyObject *PyErr_ImplementationError;
PyObject *PyErr_InsufficientMemoryError;
PyObject *plum_unpack_and_dump;
PyObject *plumunpack_from_buffer_and_dump;
PyObject *plum_pack_and_dump;
PyTypeObject *Plum_Type;
PyTypeObject *PlumMeta_Type;
PyTypeObject *PlumView_Type;
PyObject *fmt_string;
Py_hash_t fmt_hash;
PyObject *zero;


PyObject *async_method(PyObject *self) {
    PyErr_Format(
        PyExc_TypeError,
        "'%s' does not support async methods", Py_TYPE(self)->tp_name);

    return NULL;
}


inline FastStruct * get_faststruct(PyTypeObject *cls) {
    if ((cls->tp_as_async) && (cls->tp_as_async->am_anext == async_method)) {
        return (FastStruct*) cls->tp_as_async;
    }
    return NULL;
}


static Py_ssize_t pack_value(
        PyTypeObject *cls, PyObject **bytearray_retval, Py_ssize_t offset, PyObject *item, PyObject *parent) {
    tracef("PACK_VAL:ENTER");

    FastStruct *fs = get_faststruct(cls);

    Py_INCREF(item);

    dbgprintf("  PACK_VAL: offset=%ld", offset);

    if (PyObject_TypeCheck(item, PlumView_Type)) {
        tracef("  PACK_VAL:VAL_IS_VIEW");
        PyObject *result = PyObject_CallMethod((PyObject*)item, "get", NULL);
        if (result) {
            tracef("  PACK_VAL:VAL_IS_VIEW,GET_SUCCESS");
            Py_DECREF(item);
            item = result;
        }
        else {
            tracef("  PACK_VAL:VAL_IS_VIEW,GET_FAIL");
            Py_DECREF(item);
            return -1;
        }
    }

    if (fs && (fs->nbytes >= 0)) {
        tracef("  PACK_VAL:FASTDATA_AND_FIXED");
        Py_ssize_t nbytes = offset + fs->nbytes;
        dbgprintf("  PACK_VAL: offset=%ld, fs->nbytes=%ld, nbytes=%ld", offset, fs->nbytes, nbytes);
        if (*bytearray_retval) {
            tracef("  PACK_VAL:FASTDATA_AND_FIXED,BUF_EXIST");
            dbgprintf("  PACK_VAL: check resize len(m)=%ld", PyByteArray_GET_SIZE(*bytearray_retval));
            if (nbytes > PyByteArray_GET_SIZE(*bytearray_retval)) {
                tracef("  PACK_VAL:FASTDATA_AND_FIXED,BUF_EXIST,RESIZING");
                if (PyByteArray_Resize(*bytearray_retval, nbytes)) {
                    Py_DECREF(item);
                    return -1;
                }
            }
        }
        else {
            tracef("  PACK_VAL:FASTDATA_AND_FIXED,BUF_CREATE");
            *bytearray_retval = PyByteArray_FromStringAndSize(NULL, nbytes);
            if (!*bytearray_retval) {
                Py_DECREF(item);
                return -1;
            }
        }
        if (fs->pack) {
            tracef("  PACK_VAL:FASTDATA_AND_FIXED,FAST_PACK");
            offset = fs->pack(fs, cls, *bytearray_retval, offset, item, parent);
            dbgprintf("  PACK_VAL: fast pack returned offset=%ld", offset);
        }
        else {
            tracef("  PACK_VAL:FASTDATA_AND_FIXED,SLOW_PACK");
            PyObject *result = PyObject_CallMethod(
                (PyObject*)cls, "__pack__", "OnOOO",
                *bytearray_retval, offset, parent, item, Py_None);
            if (result) {
                tracef("  PACK_VAL:FASTDATA_AND_FIXED,SLOW_PACK,SUCCESS");
                /* since we already know the new offset, ignore the returned offset */
                /* (to save time by avoiding conversion Python int to a Py_size_t) */
                Py_DECREF(result);
                offset = nbytes;
            } else {
                tracef("  PACK_VAL:FASTDATA_AND_FIXED,SLOW_PACK,FAIL");
                Py_DECREF(item);
                return -1;
            }
        }
    }
    else {
        tracef("  PACK_VAL:SLOW_OR_VAR");
        if (!*bytearray_retval) {
            tracef("  PACK_VAL:SLOW_OR_VAR,BUF_CREATE");
            *bytearray_retval = PyByteArray_FromStringAndSize(NULL, 0);
            if (!*bytearray_retval) {
                Py_DECREF(item);
                return -1;
            }
        }

        if (fs && fs->pack) {
            tracef("  PACK_VAL:SLOW_OR_VAR,FAST_PACK");
            offset = fs->pack(fs, cls, *bytearray_retval, offset, item, parent);
            dbgprintf("  PACK_VAL: fast pack returned offset=%ld", offset);
        }
        else {
            tracef("  PACK_VAL:SLOW_OR_VAR,SLOW_PACK");
            PyObject *result = PyObject_CallMethod(
                (PyObject*)cls, "__pack__", "OnOOO",
                *bytearray_retval, offset, parent, item, Py_None);
            if (result) {
                tracef("  PACK_VAL:SLOW_OR_VAR,SLOW_PACK,SUCCESS");
                offset = PyLong_AsSsize_t(result);
                dbgprintf("  PACK_VAL: slow pack returned offset=%ld", offset);
                Py_DECREF(result);
            }
            else {
                tracef("  PACK_VAL:SLOW_OR_VAR,SLOW_PACK,FAIL");
                Py_DECREF(item);
                return -1;
            }
        }
    }

    dbgprintf("  PACK_VAL: returning offset=%ld", offset);
    Py_DECREF(item);
    return offset;
}


static Py_ssize_t _pack_value_with_format(
        PyObject *fmt, PyObject **bytearray_retval, Py_ssize_t offset, PyObject *value, PyObject *parent) {
    tracef("PACK_VWF:ENTER");

    if (PyObject_TypeCheck(fmt, PlumMeta_Type)) {
        tracef("  PACK_VWF:FMT_IS_PLUM");
        offset = pack_value((PyTypeObject*)fmt, bytearray_retval, offset, value, parent);
    }
    else if (PyTuple_Check(fmt) || PyList_Check(fmt)) {
        tracef("  PACK_VWF:FMT_IS_SEQ");
        if (PyTuple_Check(value) || PyList_Check(value)) {
            tracef("  PACK_VWF:FMT_IS_SEQ,VAL_IS_SEQ");
            Py_ssize_t num_items = PySequence_Size(fmt);
            if (PySequence_Size(value) != num_items) {
                tracef("  PACK_VWF:FMT_IS_SEQ,VAL_IS_SEQ,UNEQUAL_LEN");
                return -1;
            }
            for (Py_ssize_t i=0; i < num_items; i++) {
                dbgprintf("  PACK_VWF: packing item #%ld @ offset=%ld", i, offset);
                PyObject *item_fmt = PySequence_GetItem(fmt, i); /* issued reference */
                PyObject *item_value = PySequence_GetItem(value, i); /* issued reference */
                if ((!item_fmt) || (!item_value)) {
                    dbgprintf("  PACK_VWF: unexpected error indexing value or fmt");
                    Py_XDECREF(item_fmt);
                    Py_XDECREF(item_value);
                    return -1;
                }
                offset = _pack_value_with_format(item_fmt, bytearray_retval, offset, item_value, parent);
                Py_DECREF(item_fmt);
                Py_DECREF(item_value);
            }
        }
        else {
            tracef("  PACK_VWF:FMT_IS_SEQ,VAL_IS_NOT_SEQ");
            return -1;
        }
    }
    else if PyDict_Check(fmt) {
        tracef("  PACK_VWF:FMT_IS_DICT");
        if (PyDict_Check(value)) {
            tracef("  PACK_VWF:FMT_IS_DICT,VAL_IS_DICT");
            if (PyDict_Size(fmt) != PyDict_Size(value)) {
                tracef("  PACK_VWF:FMT_IS_DICT,VAL_IS_DICT,UNEQUAL_LEN");
                return -1;
            }
            PyObject *key;
            Py_ssize_t pos = 0;
            PyObject *item_fmt;

            while (PyDict_Next(fmt, &pos, &key, &item_fmt)) {
                dbgprintf("  PACK_VWF: packing item #%ld @ offset=%ld", pos, offset);
                PyObject *item_value = PyDict_GetItem(value, key); /* borrowed reference */
                if (!item_value) {
                    tracef("  PACK_VWF:FMT_IS_DICT,VAL_IS_DICT,MISSING_KEY");
                    return -1;
                }
                offset = _pack_value_with_format(item_fmt, bytearray_retval, offset, item_value, parent);
            }
        }
        else {
            tracef("  PACK_VWF:FMT_IS_DICT,VAL_NOT_DICT"); 
            return -1;
        }
    }
    else {
        tracef("  PACK_VWF:FMT_INVALID");
        return -1;
    }

    dbgprintf("  PACK_VWF: returning offset=%ld", offset);
    return offset;
}

static PyObject *pack(PyObject *module, PyObject *args, PyObject *kwds) {
    tracef("PACK:ENTER");

    PyObject *bytearray_retval = NULL;
    PyObject *fmt=NULL;
    PyObject *fmt_arg=NULL;
    PyObject *fmt_kwd=NULL;
    PyObject *kwds_value=NULL;
    PyObject *args_slice=NULL;
    PyObject *args_value=NULL;
    PyObject *parent=Py_None;
    Py_ssize_t num_args = PyTuple_GET_SIZE(args);
    Py_ssize_t num_kwds = 0;
    int retry = 0;

    Py_ssize_t offset = -1;

    if (num_args) {
        tracef("  PACK:HAS_ARGS");
        fmt = fmt_arg = PyTuple_GET_ITEM(args, 0); /* borrowed reference */
        args_value = args_slice = PyTuple_GetSlice(args, 1, num_args); /* issued reference */
        if (!args_value) {
            goto error;
        }
    }
    else {
        tracef("  PACK:NO_ARGS");
        args_value = args;
    }

    if (kwds) {
        tracef("  PACK:HAS_KWDS");
        /* make copy in case of retry */
        kwds_value = PyDict_Copy(kwds);
        if (!kwds_value) {
            goto error;
        }
        fmt_kwd = _PyDict_Pop(kwds_value, fmt_string, NULL); /* transferred reference */
        if (fmt_kwd) {
            tracef("  PACK:HAS_KWDS,FMT_KWD");
            fmt = fmt_kwd;
        }
        else {
            tracef("  PACK:HAS_KWDS,NO_FMT_KWD");
            PyErr_Clear();
        }
        num_kwds = PyDict_Size(kwds_value);
        dbgprintf("  PACK: num_kwds=%ld", num_kwds);
    }

    if (fmt_arg && fmt_kwd) {
        tracef("  PACK:HAS_DUP_FMT");
        PyErr_SetString(PyExc_TypeError, "pack() got multiple values for argument 'fmt'");
        goto error;
    }

    if (!fmt) {
        tracef("  PACK:NO_FMT");
        PyErr_SetString(PyExc_TypeError, "pack() missing 1 required positional argument: 'fmt'");
        goto error;
    }

    retry = 1;

    if (PyObject_TypeCheck(fmt, PlumMeta_Type)) {
        tracef("  PACK:FMT_IS_PLUM");
        if (num_kwds || PyTuple_GET_SIZE(args_value) != 1) {
            tracef("  PACK:FMT_IS_PLUM,EXTRA_VALUES");
            goto error;
        }
        offset = pack_value((PyTypeObject*)fmt, &bytearray_retval, 0, PyTuple_GET_ITEM(args_value, 0), parent);
    }
    else if (PyTuple_Check(fmt) || PyList_Check(fmt)) {
        tracef("  PACK:FMT_IS_SEQ");
        if (num_kwds) {
            tracef("  PACK:FMT_IS_SEQ,WITH_KWDS");
            goto error;
        }
        offset = _pack_value_with_format(fmt, &bytearray_retval, 0, args_value, parent);
    }
    else if PyDict_Check(fmt) {
        tracef("  PACK:FMT_IS_DICT");
        if (PyTuple_GET_SIZE(args_value)) {
            tracef("  PACK:FMT_IS_DICT,WITH_ARGS");
            goto error;
        }
        else if (kwds_value) {
            tracef("  FMT_IS_DICT,PACKING_KWDS");
            offset = _pack_value_with_format(fmt, &bytearray_retval, 0, kwds_value, parent);
        }
        else if (PyDict_Size(fmt)) {
            tracef("  PACK:FMT_IS_DICT,NO_VALUES");
            goto error;
        }
        else {
            /* do nothing */
            tracef("  PACK:FMT_IS_DICT,BUT_EMPTY");
            PyObject *empty_dict = PyDict_New();
            if (!empty_dict) {
                goto error;
            }
            offset = _pack_value_with_format(fmt, &bytearray_retval, 0, empty_dict, parent);
            Py_DECREF(empty_dict);
        }
    }
    else {
        tracef("  PACK:INVALID_FMT");
        goto error;
    }

    dbgprintf("  PACK:offset=%ld", offset);

    Py_XDECREF(args_slice);
    Py_XDECREF(fmt_kwd);
    Py_XDECREF(kwds_value);

    if (offset < 0) {
        tracef("  PACK:FAILED_PACK");
        goto error;
    }

    if (!bytearray_retval) {
        tracef("  PACK:NO_VALUES_PACKED");
        bytearray_retval = PyByteArray_FromStringAndSize(NULL, 0);
    }

    return bytearray_retval;

error:
    tracef("  PACK:ERROR");
    Py_XDECREF(args_slice);
    Py_XDECREF(fmt_kwd);
    Py_XDECREF(kwds_value);
    Py_XDECREF(bytearray_retval);

    if (retry) {
        tracef("  PACK:ERROR,RETRY");
        /* do it over to include dump in exception message */
        /* (performance is not a concern at this point) */
        PyErr_Clear();

        bytearray_retval = PyObject_Call(plum_pack_and_dump, args, kwds);

        if (bytearray_retval) {
            dbgprintf("  PACK:implementation error");
            PyErr_SetNone(PyErr_ImplementationError);
            Py_DECREF(bytearray_retval);
        }
    }
    
    dbgprintf("  PACK:return=NULL");
    return NULL;
};


static unsigned char *getbytes(Py_buffer *buffer, PyObject*buffer_arg, Py_ssize_t *offset, Py_ssize_t *nbytes, PyObject **bytes_object) {
    tracef("GETBYTES:ENTER");
    unsigned char *src = NULL;
    *bytes_object = NULL;
    Py_ssize_t requested_nbytes = *nbytes;

    if (buffer) {
        tracef("  GETBYTES:BYTEBUF");
        /* implementation for buffer (e.g. bytes, bytearray, etc.) */
        src = ((unsigned char *)buffer->buf) + *offset;

        if ((*nbytes < 0) || ((*offset + *nbytes) > buffer->len)) {
            tracef("  GETBYTES:BYTEBUF,NBYTES_DIFFERS");
            *nbytes = buffer->len - *offset;
        }
    }
    else {
        tracef("  GETBYTES:BINFILE");
        /* implementation for binary file (e.g. io.BytesIO) */

        if (*nbytes < 0) {
            tracef("  GETBYTES:BINFILE,READ_ALL");
            *bytes_object = PyObject_CallMethod(buffer_arg, "read", NULL);
        }
        else {
            tracef("  GETBYTES:BINFILE,READ_NBYTES");
            *bytes_object = PyObject_CallMethod(buffer_arg, "read", "n", *nbytes);
        }

        if (*bytes_object) {
            tracef("  GETBYTES:BINFILE,READ_OK");
            src = (unsigned char *) PyBytes_AS_STRING(*bytes_object);
            *nbytes = PyBytes_Size(*bytes_object);
        }
        else {
            tracef("  GETBYTES:BINFILE,READ_ERROR");
            *nbytes = -1;  /* indicate error */
        }
    }

    if (*nbytes >= 0) {
        tracef("  GETBYTES:GOT_BYTES");
        if ((requested_nbytes < 0) || (requested_nbytes == *nbytes)) {
            tracef("  GETBYTES:GOT_BYTES,OK");
            *offset += *nbytes;
        }
        else {
            tracef("  GETBYTES:GOT_BYTES,SHORTAGE");
            *nbytes = -1; /* indicate error */
            src = NULL;
        }
    }
    else {
        tracef("  GETBYTES:ERROR");
        src = NULL;
    }
    
    return src;
}


static PyObject *unpack_plum(PyTypeObject* cls, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset, PyObject *parent) {
    tracef("UNPACK_PLUM:ENTER");

    FastStruct *fs = get_faststruct(cls);
    PyObject *item;

    if (fs && fs->unpack) {
        tracef("  UNPACK_PLUM:FAST");
        Py_ssize_t references;
        references = references;  // eliminate compiler warning when debugging off
        dbgprintf("  UNPACK_PLUM: refcnt(parent)=%ld (before unpack)", Py_REFCNT(parent));
        SET_REFCOUNTS(references, parent);
        item = fs->unpack(fs, cls, buffer, buffer_arg, offset, parent);
        dbgprintf("  UNPACK_PLUM: refcnt(parent)=%ld (after unpack)", Py_REFCNT(parent));
        CMP_REFCOUNTS(references, parent);
    }
    else {
        tracef("  UNPACK_PLUM:SLOW");
        dbgprintf("  UNPACK_PLUM: refcnt(parent)=%ld, refcnt(None)=%ld (before slow unpack)", Py_REFCNT(parent), Py_REFCNT(Py_None));
        PyObject *result = PyObject_CallMethod((PyObject*)cls, "__unpack__", "OnOO", buffer_arg, *offset, parent, Py_None);
        dbgprintf("  UNPACK_PLUM: refcnt(parent)=%ld, refcnt(None)=%ld (after slow unpack)", Py_REFCNT(parent), Py_REFCNT(Py_None));
        if (result) {
            tracef("  UNPACK_PLUM:SLOW,SUCCEED");
            if (PyTuple_Size(result) == 2) {
                tracef("  UNPACK_PLUM:SLOW,SUCCEED,TUPLE_OK");
                item = PyTuple_GET_ITEM(result, 0);
                *offset = PyLong_AsSsize_t(PyTuple_GET_ITEM(result, 1));
                if (*offset < 0) {
                    tracef("  UNPACK_PLUM:SLOW,SUCCEED,TUPLE_OK,OFFSET_BAD");
                    item = NULL;
                }
                else {
                    tracef("  UNPACK_PLUM:SLOW,SUCCEED,TUPLE_OK,OFFSET_OK");
                    Py_INCREF(item);
                }
            }
            else {
                tracef("  UNPACK_PLUM:SLOW,TUPLE_BAD");
                dbgprintf("  UNPACK_PLUM: cls.__unpack__() had result but wrong type/size");
                /* raise TypeError('__unpack__() had result but wrong type/size') */
                PyErr_SetNone(PyExc_TypeError);
                item = NULL;
            }
            Py_DECREF(result);
        }
        else {
            tracef("  UNPACK_PLUM:SLOW,ERROR");
            item = NULL;
        }
    }

    return item;
};

static PyObject *unpack_list(PyObject* types, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset);
static PyObject *unpack_tuple(PyObject* types, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset);
static PyObject *unpack_dict(PyObject* types, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset);

static PyObject *unpack_item(PyObject *fmt, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset, PyObject *parent) {

    tracef("UNPACK_ITEM:ENTER");

    PyObject* item = NULL;

    if (PyObject_TypeCheck(fmt, PlumMeta_Type)) {
        tracef("  UNPACK_ITEM:PLUM");
        item = unpack_plum((PyTypeObject*)fmt, buffer, buffer_arg, offset, parent);
    }
    else if (PyTuple_Check(fmt)) {
        tracef("  UNPACK_ITEM:TUPLE");
        item = unpack_tuple(fmt, buffer, buffer_arg, offset);
    }
    else if (PyList_Check(fmt)) {
        tracef("  UNPACK_ITEM:LIST");
        item = unpack_list(fmt, buffer, buffer_arg, offset);
    }
    else if PyDict_Check(fmt) {
        tracef("  UNPACK_ITEM:DICT");
        item = unpack_dict(fmt, buffer, buffer_arg, offset);
    }
    else {
        tracef("  UNPACK_ITEM:BAD_FMT");
    }

    return item;
}

static PyObject *unpack_list(PyObject* types, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset) {

    tracef("UNPACK_LIST:ENTER");

    Py_ssize_t numitems = PyList_GET_SIZE(types);

    dbgprintf("  UNPACK_LIST: numitems = %ld", numitems);

    PyObject *items = PyList_New(numitems);
    if (items == NULL) {
        return NULL;
    }

    for (Py_ssize_t i=0; i < numitems; i++) {
        tracef("  UNPACK_LIST:FOR");
        PyObject *cls = PyList_GET_ITEM(types, i);

        PyObject *item = unpack_item(cls, buffer, buffer_arg, offset, Py_None);

        if (item == NULL) {
            tracef("  UNPACK_LIST:FOR,ITEM_BAD");
            dbgprintf("  UNPACK_LIST: item did not unpack, throwing list away");
            Py_DECREF(items);
            items = NULL;
            break;
        }
        else {
            tracef("UNPACK_LIST:FOR,ITEM_OK");
            PyList_SET_ITEM(items, i, item);
        }
    }

    return items;
};

static PyObject *unpack_tuple(PyObject* types, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset) {

    tracef("UNPACK_TUPLE:ENTER");

    Py_ssize_t numitems = PyTuple_GET_SIZE(types);
    dbgprintf("  UNPACK_TUPLE:numitems = %ld", numitems);

    PyObject *items = PyTuple_New(numitems);
    if (items == NULL) {
        return NULL;
    }

    for (Py_ssize_t i=0; i < numitems; i++) {
        tracef("  UNPACK_TUPLE:FOR");
        PyObject *cls = PyTuple_GET_ITEM(types, i);

        dbgprintf("  UNPACK_TUPLE: unpacking item %ld", i);
        PyObject *item = unpack_item(cls, buffer, buffer_arg, offset, Py_None);

        if (item == NULL) {
            tracef("  UNPACK_TUPLE:FOR,ITEM_BAD");
            dbgprintf("  UNPACK_TUPLE: item did not unpack, throwing tuple away");
            Py_DECREF(items);
            items = NULL;
            break;
        }
        else {
            tracef("  UNPACK_TUPLE:FOR,ITEM_OK");
            PyTuple_SET_ITEM(items, i, item);
        }
    }

    return items;
};

static PyObject *unpack_dict(PyObject* types, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset) {

    tracef("UNPACK_DICT:ENTER");

    PyObject *items = PyDict_New();

    if (items == NULL) {
        return NULL;
    }

    PyObject *key, *fmt;
    Py_ssize_t pos = 0;

    while (PyDict_Next(types, &pos, &key, &fmt)) {
        tracef("  UNPACK_DICT:WHILE");
        dbgprintf("  UNPACK_DICT:unpacking item %ld", pos - 1);
        PyObject *item = unpack_item(fmt, buffer, buffer_arg, offset, Py_None);

        if (item) {
            tracef("  UNPACK_DICT:WHILE,ITEM_OK");
            if (PyDict_SetItem(items, key, item)) {
                dbgprintf("  UNPACK_DICT:item did not insert into dict, clearing dict");
                Py_DECREF(items);
                return NULL;
            }
            Py_DECREF(item); /* PyDict_SetItem() doesn't steal reference */
        }
        else {
            tracef("  UNPACK_DICT:WHILE,ITEM_BAD");
            Py_DECREF(items);
            return NULL;
       }
    }

    return items;
};

static PyObject *unpack_from_buffer(PyObject *fmt, PyObject *buffer_arg, PyObject *offset_arg, int check_excess) {
    Py_buffer _buffer;
    Py_buffer *buffer;
    Py_ssize_t offset=0;

    tracef("UNPACK_FB:ENTER");

    if (PyObject_GetBuffer(buffer_arg, &_buffer, PyBUF_SIMPLE)) {
        tracef("  UNPACK_FB:BINFILE");
        /* not bytes-like must be binary file */
        PyErr_Clear();

        buffer = NULL;

        if (offset_arg == Py_None) {
            tracef("  UNPACK_FB:BINFILE,TELL_OFF");
            PyObject *tell_value = PyObject_CallMethod(buffer_arg, "tell", NULL);
            if (!tell_value) {
                tracef("  UNPACK_FB:BINFILE,TELL_OFF,FAIL");
                return NULL;
            }
            tracef("  UNPACK_FB:BINFILE,TELL_OFF,SUCCEED");
            offset = PyLong_AsSsize_t(tell_value);
            dbgprintf("  UNPACK_FB: tell offset = %ld", offset);
            Py_DECREF(tell_value);
            if (offset == -1) {
                return NULL;
            }
        }
        else {
            tracef("  UNPACK_FB:BINFILE,OFF_ARG");

            offset = PyLong_AsSsize_t(offset_arg);
            if (offset == -1) {
                tracef("  UNPACK_FB:BINFILE,OFF_ARG,BAD");
                return NULL;
            }
            dbgprintf("  UNPACK_FB: offset=%ld", offset);

            PyObject *none_value = PyObject_CallMethod(buffer_arg, "seek", "O", offset_arg, NULL);
            Py_XDECREF(none_value);
            if (!none_value) {
                tracef("  UNPACK_FB:BINFILE,OFF_ARG,SEEK_FAIL");
                return NULL;
            }
            tracef("  UNPACK_FB:BINFILE,OFF_ARG,SEEK_OK");
        }
    }
    else {
        tracef("  UNPACK_FB:BYTEBUF");
        buffer = &_buffer;
        if (offset_arg == Py_None) {
            tracef("  UNPACK_FB:BYTEBUF,DEFAULT_OFFSET");
            offset = 0;
        }
        else {
            tracef("  UNPACK_FB:BYTEBUF,OFFSET_ARG");
            offset = PyLong_AsSsize_t(offset_arg);
            if (offset == -1) {
                tracef("  UNPACK_FB:BYTEBUF,OFFSET_ARG,BAD");
                PyBuffer_Release(buffer);
                return NULL;
            }
            tracef("  UNPACK_FB:BYTEBUF,OFFSET_ARG,OK");
            dbgprintf("  UNPACK_FB: offset=%ld", offset);
        }
    }

    Py_ssize_t offset_copy = offset;  /* in case of re-do */

    PyObject *values = unpack_item(fmt, buffer, buffer_arg, &offset_copy, Py_None);

    if (values && check_excess) {
        tracef("  UNPACK_FB:CHECK_EXCESS");
        Py_ssize_t num_excess_bytes;
        if (buffer) {
            tracef("  UNPACK_FB:CHECK_EXCESS,BYTEBUF");
            num_excess_bytes = buffer->len - offset_copy;
        }
        else {
            tracef("  UNPACK_FB:CHECK_EXCESS,BINFILE");
            PyObject *leftover = PyObject_CallMethod(buffer_arg, "read", NULL);
            if (leftover) {
                tracef("  UNPACK_FB:CHECK_EXCESS,BINFILE,READ_OK");
                num_excess_bytes = Py_SIZE(leftover);
                Py_DECREF(leftover);
            }
            else {
                tracef("  UNPACK_FB:CHECK_EXCESS,BINFILE,READ_FAIL");
                num_excess_bytes = 1;  /* recycle normal ref count / error handling */
            }
        }

        dbgprintf("  UNPACK_FB: num_excess_bytes = %ld", num_excess_bytes);

        if (num_excess_bytes) {
            tracef("  UNPACK_FB:CHECK_EXCESS,ERROR");
            Py_DECREF(values);
            values = NULL;
        }
    }

    if (buffer) {
        tracef("  UNPACK_FB:RELEASE_BUF");
        PyBuffer_Release(buffer);
    }

    if (!values) {
        tracef("  UNPACK_FB:ERROR");
        /* prepare to re-do operation and generate exception using plum-py utility */
        /* (speed no longer important) */
        PyErr_Clear();
        if (!buffer) {
            tracef("  UNPACK_FB:ERROR,SEEK");
            /* rewind binary file to where we started */
            PyObject *none_value = PyObject_CallMethod(buffer_arg, "seek", "n", offset, NULL);
            Py_XDECREF(none_value);
        }
    }

    return values;
}

static PyObject *unpack_from(PyObject *module, PyObject *args, PyObject *kwds) {
    PyObject *fmt;
    PyObject *buffer_arg;
    PyObject *offset_arg = Py_None;

    tracef("UNPACK_FROM:ENTER");

    static char *kwlist[] = {"fmt", "buffer", "offset", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "OO|O", kwlist, (PyObject**) &fmt, &buffer_arg, &offset_arg)) {
        tracef("  UNPACK_FROM:KW_FAIL");
        return NULL;
    }

    PyObject *values = unpack_from_buffer(fmt, buffer_arg, offset_arg, 0);

    if (!values) {
        tracef("  UNPACK_FROM:ERROR");
        /* re-do operation and generate exception using plum-py utility */
        /* (speed no longer important) */
        PyErr_Clear();
        values = PyObject_CallFunction(plumunpack_from_buffer_and_dump, "OOO", (PyObject*) fmt, buffer_arg, offset_arg);
        if (values) {
            PyErr_SetNone(PyErr_ImplementationError);
            Py_DECREF(values);
            return NULL;
        }
    }

    dbgprintf("unpack_from() returning values %p", values);

    return values;
};


static PyObject *unpack(PyObject *self, PyObject *args)
{
    PyObject *fmt;  /* borrowed ref */
    PyObject *buffer_arg;  /* borrowed ref */

    tracef("UNPACK:ENTER");
    
    if (!PyArg_UnpackTuple(args, "unpack", 2, 2, &fmt, &buffer_arg)) {
        tracef("  UNPACK:POS_FAIL");
        return NULL; 
    }

    PyObject *values = unpack_from_buffer(fmt, buffer_arg, zero, 1);

    if (!values) {
        tracef("  UNPACK:ERROR");
        /* re-do operation and generate exception using plum-py utility */
        /* (speed no longer important) */
        PyErr_Clear();
        values = PyObject_CallFunction(plum_unpack_and_dump, "OO", (PyObject*) fmt, buffer_arg);

        if (values) {
            PyErr_SetNone(PyErr_ImplementationError);
            Py_DECREF(values);
            values = NULL;
        }
    }

    return values;
};


static void fill_faststruct(PyTypeObject *cls, FastStruct *fs) {

    cls->tp_as_async = (PyAsyncMethods*) fs;
    fs->am.am_await = NULL;
    fs->am.am_aiter = NULL;
    fs->am.am_anext = async_method;
    fs->nbytes = -1;
    fs->unpack = NULL;
    fs->pack = NULL;
};

static FastUtilsStruct fastutils = {
    fill_faststruct,
    getbytes,
    pack_value,
    unpack_item,
};


static PyObject *
c_api_get_fastutils_pointer(PyObject *self, PyObject *Py_UNUSED(ignored))
{
    FastUtilsStruct *ptr = &fastutils;
    return PyBytes_FromStringAndSize((char *) &ptr, sizeof(ptr));
}

static PyMethodDef ExtModMethods[] = {
    {"c_api_get_fastutils_pointer", c_api_get_fastutils_pointer, METH_NOARGS,
     ""},
    {"pack", (PyCFunction)pack, METH_VARARGS|METH_KEYWORDS,
     pack_docstring},
    {"unpack", (PyCFunction)unpack, METH_VARARGS,
     unpack_docstring},
    {"unpack_from", (PyCFunction)unpack_from, METH_VARARGS|METH_KEYWORDS,
     unpack_from_docstring},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static PyModuleDef utils_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "plum_boost._utils",
    .m_doc = "Pack/Unpack Memory utility functions.",
    .m_size = -1,
    .m_methods = ExtModMethods,
};

PyMODINIT_FUNC PyInit__utils(void) {
    fmt_string = NULL;
    zero = NULL;

    fmt_string = PyUnicode_FromStringAndSize("fmt", 3);
    if (!fmt_string) {
       return NULL;
    }

    zero = PyLong_FromLong(0);
    if (!zero) {
        goto error;
    }


    fmt_hash = PyObject_Hash(fmt_string);
    if (fmt_hash == -1) {
        goto error;
    }

    /*
    from plum import unpack as plum_unpack_and_dump
    */

    PyObject *plum_module = PyImport_ImportModule("plum"); /* issued */
    if (plum_module == NULL) {
        goto error;
    }

    PyObject *plum_module_dict = PyModule_GetDict(plum_module); /* borrowed */
    Py_XDECREF(plum_module);
    if (plum_module_dict == NULL) {
        goto error;
    }

    Plum_Type = (PyTypeObject*) PyDict_GetItemString(plum_module_dict, "Plum"); /* borrowed */
    if (Plum_Type == NULL) {
        goto error;
    }

    PlumView_Type = (PyTypeObject*) PyDict_GetItemString(plum_module_dict, "PlumView"); /* borrowed */
    if (PlumView_Type == NULL) {
        goto error;
    }

    PlumMeta_Type = (PyTypeObject*) PyDict_GetItemString(plum_module_dict, "PlumType"); /* borrowed */
    if (PlumMeta_Type == NULL) {
        goto error;
    }

    plum_pack_and_dump = PyDict_GetItemString(plum_module_dict, "pack_and_dump"); /* borrowed */
    if (plum_pack_and_dump == NULL) {
        goto error;
    }

    plum_unpack_and_dump = PyDict_GetItemString(plum_module_dict, "unpack_and_dump"); /* borrowed */
    if (plum_unpack_and_dump == NULL) {
        goto error;
    }

    plumunpack_from_buffer_and_dump = PyDict_GetItemString(plum_module_dict, "unpack_from_and_dump"); /* borrowed */
    if (plum_unpack_and_dump == NULL) {
        goto error;
    }

    /*
    from plum._exceptions import ImplementationError
    */

    PyObject *exc_module = PyImport_ImportModule("plum._exceptions"); /* issued */
    if (exc_module == NULL) {
        goto error;
    }

    PyObject *exc_module_dict = PyModule_GetDict(exc_module); /* borrowed */
    Py_XDECREF(exc_module);
    if (exc_module_dict == NULL) {
        goto error;
    }

    PyErr_ExcessMemoryError = PyDict_GetItemString(exc_module_dict, "ExcessMemoryError"); /* borrowed */
    if (PyErr_ExcessMemoryError == NULL) {
        goto error;
    }

    PyErr_ImplementationError = PyDict_GetItemString(exc_module_dict, "ImplementationError"); /* borrowed */
    if (PyErr_ImplementationError == NULL) {
        goto error;
    }

    PyErr_InsufficientMemoryError = PyDict_GetItemString(exc_module_dict, "InsufficientMemoryError"); /* borrowed */
    if (PyErr_InsufficientMemoryError == NULL) {
        goto error;
    }

    /*
    Create module.
    */

    PyObject *this_module = PyModule_Create(&utils_module); /* issued (give to caller) */
    if (this_module != NULL) {
        Py_INCREF(this_module); /* never allow this module to be deleted */
        Py_INCREF(Plum_Type);
        Py_INCREF(PlumMeta_Type);
        Py_INCREF(PlumView_Type);
        Py_INCREF(plum_pack_and_dump);
        Py_INCREF(plum_unpack_and_dump);
        Py_INCREF(plumunpack_from_buffer_and_dump);
        Py_INCREF(PyErr_ExcessMemoryError);
        Py_INCREF(PyErr_ImplementationError);
        Py_INCREF(PyErr_InsufficientMemoryError);
    }

    return this_module;
    
error:
    Py_XDECREF(fmt_string);
    Py_XDECREF(zero);

    return NULL;

}
