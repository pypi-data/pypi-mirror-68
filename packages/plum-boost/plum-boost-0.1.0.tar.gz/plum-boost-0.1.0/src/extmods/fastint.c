#include <Python.h>
#include "structmember.h"

#include "fast.h"

typedef struct {
    FastStruct fs;
    int little_endian;
    int is_signed;
    int unpack_int;
    int strict;
} FastIntStruct;

static FastUtilsStruct *fastutils;

static Py_ssize_t pack(void *fs, PyTypeObject* cls, PyObject *bytearray_retval, Py_ssize_t offset, PyObject *item, PyObject *parent) {
    tracef("INT_PACK:ENTER");

    FastIntStruct *fis = (FastIntStruct*) fs;

    Py_ssize_t nbytes = fis->fs.nbytes;

    unsigned char *dst = (unsigned char *) &PyByteArray_AS_STRING(bytearray_retval)[offset];

    if ((fis->strict) && (item->ob_type != cls)) {
        tracef("  INT_PACK:VERIFY_STRICT");

        /* ensure what is being packed is a valid enumeration value */
        PyObject *temp = PyObject_CallFunctionObjArgs((PyObject*)cls, item, NULL); /* issued */
        Py_XDECREF(temp);
        if (!temp) {
            tracef("  INT_PACK:VERIFY_STRICT,NOT_MEMBER");
            return -1;
        }
    }

    if (_PyLong_AsByteArray((PyLongObject*)item, dst, nbytes, fis->little_endian, fis->is_signed)) {
        tracef("  INT_PACK:ERROR");
        return -1;
    }

    dbgprintf("  INT_PACK:successful, returning offset=%ld", offset + nbytes);

    return offset + nbytes;
}


static PyObject* unpack(void *fs, PyTypeObject* cls, Py_buffer *buffer, PyObject *buffer_arg, Py_ssize_t *offset, PyObject *parent) {
    FastIntStruct *fis = (FastIntStruct*) fs;
    PyObject *bytes_object = NULL;
    Py_ssize_t nbytes = fis->fs.nbytes;
    PyObject *long_obj = NULL;

    tracef("INT_UNPACK:ENTER");

    unsigned char *src = fastutils->getbytes(buffer, buffer_arg, offset, &nbytes, &bytes_object);

    if (nbytes == fis->fs.nbytes) {
        tracef("  INT_UNPACK:GET_INT");
        long_obj = _PyLong_FromByteArray(src, fis->fs.nbytes, fis->little_endian, fis->is_signed);
    }

    /* release bytes object read from binary file (if applicable) */
    Py_XDECREF(bytes_object);

    PyObject *result;

    if (long_obj) {
        tracef("  INT_UNPACK:INT_OK");
        if (fis->unpack_int) {
            tracef("  INT_UNPACK:INT_OK,KEEP_AS_INT");
            result = long_obj;
        }
        else {
            tracef("  INT_UNPACK:INT_OK,CONVERT");
            result = PyObject_CallFunctionObjArgs((PyObject*)cls, long_obj, NULL); /* issued */
            if (result) {
                tracef("  INT_UNPACK:INT_OK,CONVERT,OK");
                Py_XDECREF(long_obj);
            }
            else {
                tracef("  INT_UNPACK:INT_OK,CONVERT,FAIL");
                if (fis->strict) {
                    tracef("  INT_UNPACK:INT_OK,CONVERT,FAIL,STRICT");
                    Py_XDECREF(long_obj);
                }
                else {
                    tracef("  INT_UNPACK:INT_OK,CONVERT,FAIL,ACCEPTABLE");
                    PyErr_Clear();
                    result = long_obj;
                }
            }
        }
    }
    else {
        tracef("  INT_UNPACK:INT_BAD");
        result = NULL;
    }

    return result;
}


PyObject *add_c_acceleration(PyObject *self, PyObject *args) {

    FastIntStruct fis;
    PyTypeObject *cls;
    Py_ssize_t nbytes;

    if (!PyArg_ParseTuple(args, "Oniiii", (PyObject**)&cls, &nbytes, &fis.little_endian,
                          &fis.is_signed, &fis.unpack_int, &fis.strict)) {
        return NULL;
    }

    PyObject* nugget = PyBytes_FromStringAndSize((char *) &fis, sizeof(FastIntStruct));

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
     "integer pack/unpack accelerator"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static PyModuleDef fastint_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "plum_boost._fastint",
    .m_doc = "Pack/Unpack Integer accelerators.",
    .m_size = -1,
    .m_methods = ExtModMethods,
};


PyMODINIT_FUNC PyInit__fastint(void) {
    /*
    from plum_boost._utils import c_api_get_fastutils_pointer
    fastutils = c_api_get_fastutils_pointer()
    */

    PyObject *c_utils_module = PyImport_ImportModule("plum_boost._utils"); /* issued */
    if (!c_utils_module) {
        return NULL;
    }

    PyObject *c_utils_module_dict = PyModule_GetDict(c_utils_module); /* borrowed */
    Py_XDECREF(c_utils_module);
    if (!c_utils_module_dict) {
        return NULL;
    }

    PyObject *c_api_callable = PyDict_GetItemString(c_utils_module_dict, "c_api_get_fastutils_pointer"); /* borrowed */
    if (!c_api_callable) {
        return NULL;
    }
    PyObject *c_api_pointer_string = PyObject_CallObject(c_api_callable, NULL); /* issued */
    if (!c_api_pointer_string) {
        return NULL;
    }
    fastutils = *((FastUtilsStruct**)PyBytes_AS_STRING(c_api_pointer_string));
    Py_DECREF(c_api_pointer_string);

    /*
    Create module.
    */

    PyObject *this_module = PyModule_Create(&fastint_module); /* issued (give to caller) */
    if (this_module) {
        Py_INCREF(this_module); /* never allow this module to be deleted */
    }
    
    return this_module;
}
