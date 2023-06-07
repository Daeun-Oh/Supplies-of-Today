#include <python.h>

static PyObject* compare_dict_value(PyObject* self, PyObject* args)
{
    PyObject* dict_obj;
    const char* key_str;
    const char* value_str;

    if (!PyArg_ParseTuple(args, "Oss", &dict_obj, &key_str, &value_str))
        return NULL;

    if (!PyDict_Check(dict_obj)) {
        PyErr_SetString(PyExc_TypeError, "First argument must be a dictionary.");
        return NULL;
    }

    PyObject* key_obj = PyUnicode_FromString(key_str);
    if (key_obj == NULL)
        return NULL;

    PyObject* value_obj = PyDict_GetItem(dict_obj, key_obj);
    Py_DECREF(key_obj);

    if (value_obj == NULL) {
        Py_INCREF(Py_False);
        return Py_False;
    }

    const char* actual_value_str = PyUnicode_AsUTF8(value_obj);
    int result = strcmp(actual_value_str, value_str) == 0;

    if (result)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyMethodDef ComparingKeyValMethods[] = {
    {"compare_dict_value", compare_dict_value, METH_VARARGS, "Compare dictionary value with given key and value."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef comparingkvmodule = {
    PyModuleDef_HEAD_INIT,
    "comparingkv",
    "Module for comparing dictionary value with key and value.",
    -1,
    ComparingKeyValMethods
};

PyMODINIT_FUNC PyInit_comparingkv(void)
{
    return PyModule_Create(&comparingkvmodule);
}
