#include <Python.h>
#include "structmember.h"

#include "fast.h"

typedef struct {
    FastStruct fs;
    Py_ssize_t nitems;
    PyObject *types;
} FastStructureStruct;

static FastUtilsStruct *fastutils;

static PyObject *empty_args;

static Py_ssize_t pack(
        void *fs, PyTypeObject* cls, PyObject *bytearray_retval, Py_ssize_t offset, PyObject *sequence, PyObject *parent) {

    PyObject *sequence_copy=NULL;
    PyObject *sequence_instance=NULL;

    FastStructureStruct *fis = (FastStructureStruct*) fs;
    tracef("STRUCT_PACK:ENTER");

    if (PyList_Check(sequence) || PyTuple_Check(sequence)) {
        tracef("  STRUCT_PACK:TYPE_SEQ");
        Py_ssize_t nitems = PySequence_Size(sequence);
        if (nitems == fis->nitems) {
            tracef("  STRUCT_PACK:TYPE_SEQ,RIGHT_SIZE");
        }
        else {
            tracef("  STRUCT_PACK:TYPE_SEQ,WRONG_SIZE");
            goto error;
        }
    } 
    else if (PyDict_Check(sequence)) {
        /* construct instance to assemble members in order and fill in missing members */
        tracef("  STRUCT_PACK:TYPE_DICT");
        sequence = sequence_instance = PyObject_Call((PyObject*)cls, empty_args, sequence); /* issued ref */
        if (!sequence_instance) {
            tracef("  STRUCT_PACK:TYPE_DICT,BAD_KEYWORDS");
            goto error;
        }
    }
    else {
        tracef("  STRUCT_PACK:TYPE_BAD");
        PyErr_SetString(PyExc_TypeError, "must be a list, tuple, or dict");
        goto error;
    }

    for (Py_ssize_t i=0; i < fis->nitems; i++) {
        PyTypeObject *item_type = (PyTypeObject *)PyTuple_GET_ITEM(fis->types, i);
        PyObject *item = PySequence_GetItem(sequence, i);
        if (!item) {
            goto error;
        }

        offset = fastutils->pack_value(item_type, &bytearray_retval, offset, item, sequence);
        Py_DECREF(item);
        if (offset < 0) {
            tracef("  STRUCT_PACK:ITEM_FAIL");
            goto error;
        }
    }

    Py_XDECREF(sequence_copy);
    Py_XDECREF(sequence_instance);

    return offset;

error:
    Py_XDECREF(sequence_copy);
    Py_XDECREF(sequence_instance);

    return -1;
}


static PyObject* unpack(void *fs, PyTypeObject* cls, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset, PyObject *parent) {
    tracef("STRUCT_UNPACK:ENTER");
    PyObject *value=NULL;

    FastStructureStruct *fis = (FastStructureStruct*) fs;

    value = cls->tp_new(cls, fis->types, NULL);

    if (!value) {
        dbgprintf("  STRUCT_UNPACK -> creating new structure instance failed!");
        goto error;
    }

    for (Py_ssize_t i=0; i<fis->nitems; i++) {

        PyTypeObject *item_cls = (PyTypeObject *)PyTuple_GET_ITEM(fis->types, i);

        PyObject *item = fastutils->unpack_item((PyObject*)item_cls, buffer, buffer_arg, offset, value);

        if ((!item) || (*offset < 0)) {
            tracef("  STRUCT_UNPACK:ITEM_FAIL");
            Py_XDECREF(item);
            goto error;
        }

        if (PyList_Append(value, item)) {
            dbgprintf("  STRUCT_UNPACK -> append item failed!");
            Py_DECREF(item);
            goto error;
        }

        Py_DECREF(item);

    }

    return value;

error:
    Py_XDECREF(value);
    *offset = -1;
    return NULL;
}


PyObject *add_c_acceleration(PyObject *self, PyObject *args) {

    FastStructureStruct fis;
    PyTypeObject *cls;
    Py_ssize_t nbytes;

    if (!PyArg_ParseTuple(args, "OnnO", (PyObject**)&cls, &nbytes, &fis.nitems, &fis.types)) {
        return NULL;
    }

    PyObject* nugget = PyBytes_FromStringAndSize((char *) &fis, sizeof(FastStructureStruct));

    if (nugget) {
        FastStruct *fs = (FastStruct *) PyBytes_AS_STRING(nugget);
        fastutils->fill_faststruct(cls, fs);
        fs->nbytes = nbytes;
        fs->pack = pack;
        fs->unpack = unpack;
    }

    return nugget;
};

static PyMethodDef ExtModMethods[] = {
    {"add_c_acceleration", add_c_acceleration, METH_VARARGS,
     "structure pack/unpack accelerator"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static PyModuleDef faststructure_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "plum_boost._faststructure",
    .m_doc = "Pack/Unpack Sequence accelerators.",
    .m_size = -1,
    .m_methods = ExtModMethods,
};


PyMODINIT_FUNC PyInit__faststructure(void) {
    /*
    from plum_boost._utils import c_api_get_fastutils_pointer
    fastutils = c_api_get_fastutils_pointer()
    */
    PyObject *c_api_pointer_string = NULL;

    empty_args = PyTuple_New(0);
    if (!empty_args) {
        goto error;
    }

    PyObject *c_utils_module = PyImport_ImportModule("plum_boost._utils"); /* issued */
    if (!c_utils_module) {
        goto error;
    }

    PyObject *c_utils_module_dict = PyModule_GetDict(c_utils_module); /* borrowed */
    Py_XDECREF(c_utils_module);
    if (!c_utils_module_dict) {
        goto error;
    }

    PyObject *c_api_callable = PyDict_GetItemString(c_utils_module_dict, "c_api_get_fastutils_pointer"); /* borrowed */
    if (!c_api_callable) {
        goto error;
    }
    c_api_pointer_string = PyObject_CallObject(c_api_callable, NULL); /* issued - hold onto this*/
    if (!c_api_pointer_string) {
        goto error;
    }
    fastutils = *((FastUtilsStruct**)PyBytes_AS_STRING(c_api_pointer_string));

    /*
    Create module.
    */

    PyObject *this_module = PyModule_Create(&faststructure_module); /* issued (give to caller) */
    if (this_module) {
        Py_INCREF(this_module); /* never allow this module to be deleted */
    }
    else {
        goto error;
    }
    
    return this_module;

error:
    Py_XDECREF(empty_args);
    Py_XDECREF(c_api_pointer_string);
    return NULL;
}
