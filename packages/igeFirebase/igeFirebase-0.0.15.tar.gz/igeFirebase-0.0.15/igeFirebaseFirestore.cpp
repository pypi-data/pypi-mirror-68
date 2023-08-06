#include "igeFirebase.h"
#include "igeFirebase_doc_en.h"


PyObject* firebaseFirestore_new(PyTypeObject* type, PyObject* args, PyObject* kw)
{
	firebaseFirestore_obj* self = NULL;

	self = (firebaseFirestore_obj*)type->tp_alloc(type, 0);
	self->firebaseFirestore = FirebaseFirestore::Instance();

	return (PyObject*)self;
}

void firebaseFirestore_dealloc(firebaseFirestore_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* firebaseFirestore_str(firebaseFirestore_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "firebase firestore object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* firebaseFirestore_Init(firebaseFirestore_obj* self)
{
	FirebaseFirestore::Instance()->init();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseFirestore_Release(firebaseFirestore_obj* self)
{
	FirebaseFirestore::Instance()->release();

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseFirestore_Get(firebaseFirestore_obj* self, PyObject *args)
{
	PyObject *firestoreCB = nullptr;
	char* collection = nullptr;
	char* field = nullptr;

	if (!PyArg_ParseTuple(args, "szO", &collection, &field, &firestoreCB))	return NULL;

	if (!PyCallable_Check(firestoreCB))
	{
		PyErr_SetString(PyExc_TypeError, "Callback function must be a callable object!");
		return NULL;
	}
	if(field == nullptr)
	{
		FirebaseFirestore::Instance()->Get(collection, firestoreCB);
	}
	else
	{
		FirebaseFirestore::Instance()->Get(collection, field, firestoreCB);
	}

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseFirestore_Set(firebaseFirestore_obj* self, PyObject *args, PyObject* kwargs)
{
	PyObject *firestoreCB = nullptr;
	char* collection = nullptr;
	char* field = nullptr;
	PyObject* value = nullptr;
    int timestamp = 0;
    
    static const char* kwlist[] = { "collection", "field", "value", "callback", "timestamp", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "ssO|Oi", const_cast<char **>(kwlist), &collection, &field, &value, &firestoreCB, &timestamp))	return NULL;

	FirebaseFirestore::Instance()->Set(collection, field, value, firestoreCB, timestamp);

	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* firebaseFirestore_Delete(firebaseFirestore_obj* self, PyObject *args)
{
    char* collection = nullptr;
    char* field = nullptr;
    PyObject* firestoreCB = nullptr;

    if (!PyArg_ParseTuple(args, "sz|O", &collection, &field, &firestoreCB))	return NULL;
    if(field == nullptr)
	{
		FirebaseFirestore::Instance()->Delete(collection, firestoreCB);
	}
	else
	{
		FirebaseFirestore::Instance()->Delete(collection, field, firestoreCB);
	}

    Py_INCREF(Py_None);
    return Py_None;
}

PyMethodDef firebaseFirestore_methods[] = {
	{ "init", (PyCFunction)firebaseFirestore_Init, METH_NOARGS, firebaseFirestoreInit_doc },
	{ "release", (PyCFunction)firebaseFirestore_Release, METH_NOARGS, firebaseFirestoreRelease_doc },
	{ "get", (PyCFunction)firebaseFirestore_Get, METH_VARARGS, firebaseFirestoreGet_doc },
	{ "set", (PyCFunction)firebaseFirestore_Set, METH_VARARGS | METH_KEYWORDS, firebaseFirestoreSet_doc },
    { "delete", (PyCFunction)firebaseFirestore_Delete, METH_VARARGS, firebaseFirestoreDelete_doc },
	{ NULL,	NULL }
};

PyGetSetDef firebaseFirestore_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject FirebaseFirestoreType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeFirebase.firestore",					/* tp_name */
	sizeof(firebaseFirestore_obj),				/* tp_basicsize */
	0,											/* tp_itemsize */
	(destructor)firebaseFirestore_dealloc,		/* tp_dealloc */
	0,											/* tp_print */
	0,											/* tp_getattr */
	0,											/* tp_setattr */
	0,											/* tp_reserved */
	0,											/* tp_repr */
	0,											/* tp_as_number */
	0,											/* tp_as_sequence */
	0,											/* tp_as_mapping */
	0,											/* tp_hash */
	0,											/* tp_call */
	(reprfunc)firebaseFirestore_str,			/* tp_str */
	0,											/* tp_getattro */
	0,											/* tp_setattro */
	0,											/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,							/* tp_flags */
	0,											/* tp_doc */
	0,											/* tp_traverse */
	0,											/* tp_clear */
	0,											/* tp_richcompare */
	0,											/* tp_weaklistoffset */
	0,											/* tp_iter */
	0,											/* tp_iternext */
	firebaseFirestore_methods,					/* tp_methods */
	0,											/* tp_members */
	firebaseFirestore_getsets,					/* tp_getset */
	0,											/* tp_base */
	0,											/* tp_dict */
	0,											/* tp_descr_get */
	0,											/* tp_descr_set */
	0,											/* tp_dictoffset */
	0,											/* tp_init */
	0,											/* tp_alloc */
	firebaseFirestore_new,						/* tp_new */
	0,											/* tp_free */
};
