# Time Complexity of list, set, dict https://wiki.python.org/moin/TimeComplexity

>>> from dis import dis
>>> 
>>> c1 = '"hello" == "HELLO"'
>>> c1 = compile(c1, '', 'exec')
>>> dis(c1)
  1           0 LOAD_CONST               0 ('hello')
              3 LOAD_CONST               1 ('HELLO')
              6 COMPARE_OP               2 (==)
              9 POP_TOP             
             10 LOAD_CONST               2 (None)
             13 RETURN_VALUE        
>>> c2 = '3 in [1,2,3]'
>>> c2 = compile(c2, '', 'exec')
>>> dis(c2)
  1           0 LOAD_CONST               0 (3)
              3 LOAD_CONST               4 ((1, 2, 3))
              6 COMPARE_OP               6 (in)
              9 POP_TOP             
             10 LOAD_CONST               3 (None)
             13 RETURN_VALUE        
>>> 


PyObject *
PyEval_EvalFrameEx(PyFrameObject *f, int throwflag)
{
        TARGET(COMPARE_OP)
        {
            w = POP();
            v = TOP();
            if (PyInt_CheckExact(w) && PyInt_CheckExact(v)) {
            }
            else {
              slow_compare:
                x = cmp_outcome(oparg, v, w);
            }
            Py_DECREF(v);
            Py_DECREF(w);
            SET_TOP(x);
            if (x == NULL) break;
            PREDICT(POP_JUMP_IF_FALSE);
            PREDICT(POP_JUMP_IF_TRUE);
            DISPATCH();
        }

}


static PyObject *
cmp_outcome(int op, register PyObject *v, register PyObject *w)
{
    int res = 0;
    switch (op) {
    case PyCmp_IS:
        res = (v == w);
        break;
    case PyCmp_IS_NOT:
        res = (v != w);
        break;
    case PyCmp_IN:
        res = PySequence_Contains(w, v);
        if (res < 0)
            return NULL;
        break;
    case PyCmp_NOT_IN:
        res = PySequence_Contains(w, v);
        if (res < 0)
            return NULL;
        res = !res;
        break;
    case PyCmp_EXC_MATCH:
        if (PyTuple_Check(w)) {
        }
        res = PyErr_GivenExceptionMatches(v, w);
        break;
    default:
        return PyObject_RichCompare(v, w, op);
    }
    v = res ? Py_True : Py_False;
    Py_INCREF(v);
    return v;
}


int
PySequence_Contains(PyObject *seq, PyObject *ob)
{
    Py_ssize_t result;
    if (PyType_HasFeature(seq->ob_type, Py_TPFLAGS_HAVE_SEQUENCE_IN)) {
        PySequenceMethods *sqm = seq->ob_type->tp_as_sequence;
        if (sqm != NULL && sqm->sq_contains != NULL)
            return (*sqm->sq_contains)(seq, ob);
    }
    result = _PySequence_IterSearch(seq, ob, PY_ITERSEARCH_CONTAINS);
    return Py_SAFE_DOWNCAST(result, Py_ssize_t, int);
}


sqm->sq_contains is
- string_as_sequence.string_contains, stringlib_contains_obj(),
    fastsearch() http://effbot.org/zone/stringlib.htm
- list_as_sequence.list_contains, which loop the whole array O(n)
- set_as_sequence.set_contains, which hash the key and lookup it in O(1)


PyTypeObject PyString_Type = {};

PyTypeObject PyList_Type = {};

PyTypeObject PySet_Type = {};
