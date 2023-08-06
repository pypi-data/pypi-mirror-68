#include "FirebaseFirestore.h"

FirebaseFirestore* FirebaseFirestore::instance = nullptr;
using namespace firebase;
using firebase::firestore::Firestore;

FirebaseFirestore::FirebaseFirestore()
{
	LOG("FirebaseFirestore()");
}
FirebaseFirestore::~FirebaseFirestore()
{
	LOG("~FirebaseFirestore()");
}

void FirebaseFirestore::init()
{
	
}

void FirebaseFirestore::release()
{
}

void FirebaseFirestore::Get(const char* collection, const char* field, PyObject *callback)
{
    std::string documentStr = std::string(collection) + "/" + GetImpl()->GetUserUID();
#if !defined(_WIN32)
	firebase::firestore::DocumentReference document_ref = Firestore::GetInstance()->Document(documentStr.c_str());
	Py_INCREF(callback);
	document_ref.Get().OnCompletion([collection, field, callback, this](const Future<firebase::firestore::DocumentSnapshot>& future) {
		if (future.error() == firebase::firestore::kOk) {
			const firestore::DocumentSnapshot *document = future.result();
			if (document->exists()) {
                m_taskQueue.dispatch( [collection, field, document, callback]() {
					PyObject *arglist;
                    if(document->Get(field).is_boolean())
                    {
                        arglist = Py_BuildValue("(ssb)", collection, field, document->Get(field).boolean_value());
                    }
                    else if(document->Get(field).is_integer())
                    {
                        arglist = Py_BuildValue("(ssi)", collection, field, document->Get(field).integer_value());
                    }
					else if(document->Get(field).is_string())
                    {
                        arglist = Py_BuildValue("(sss)", collection, field, document->Get(field).string_value().c_str());
                    }
                    else if(document->Get(field).is_double())
                    {
                        arglist = Py_BuildValue("(ssd)", collection, field, document->Get(field).double_value());
                    }
					else if(document->Get(field).is_map())
					{
						PyObject *dict(PyDict_New());
						for (const auto& kv : document->Get(field).map_value()) {

							if(kv.second.is_boolean())
							{
								PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("b", kv.second.boolean_value()));
							}
							else if(kv.second.is_integer())
							{
								PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("i", kv.second.integer_value()));
							}
							else if(kv.second.is_string())
							{
								PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("s", kv.second.string_value().c_str()));
							}
							else if(kv.second.is_double())
							{
								PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("d", kv.second.double_value()));
							}
						}
						arglist = Py_BuildValue("(ssO)", collection, field, dict);
					}
                    else
					{
						arglist = Py_BuildValue("(ssO)", collection, field, Py_None);
					}

					PyObject *result = PyEval_CallObject(callback, arglist);

					Py_DECREF(arglist);
					Py_XDECREF(result);
					Py_DECREF(callback);
			    });
			} else {
				Py_DECREF(callback);
			}
		} else {
			Py_DECREF(callback);
		}
	});
#endif
}

void FirebaseFirestore::Get(const char* collection, PyObject *callback)
{
    std::string documentStr = std::string(collection) + "/" + GetImpl()->GetUserUID();
#if !defined(_WIN32)
    firebase::firestore::DocumentReference document_ref = Firestore::GetInstance()->Document(documentStr.c_str());
    Py_INCREF(callback);
    document_ref.Get().OnCompletion([collection, callback, this](const Future<firebase::firestore::DocumentSnapshot>& future) {
        if (future.error() == firebase::firestore::kOk) {
            const firestore::DocumentSnapshot *document = future.result();
            if (document->exists()) {
                m_taskQueue.dispatch( [collection, document, callback, this]() {
                    PyObject *dict(PyDict_New());
                    for (const auto& kv : document->GetData())
                    {
                        if(kv.second.is_boolean())
                        {
                            PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("b", kv.second.boolean_value()));
                        }
                        else if(kv.second.is_integer())
                        {
                            PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("i", kv.second.integer_value()));
                        }
                        else if(kv.second.is_string())
                        {
                            PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("s", kv.second.string_value().c_str()));
                        }
                        else if(kv.second.is_double())
                        {
                            PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("d", kv.second.double_value()));
                        }
                        else if(kv.second.is_map())
                        {
                            PyObject *_dict(PyDict_New());
                            for (const auto& _kv : kv.second.map_value()) {

                                if(_kv.second.is_boolean())
                                {
                                    PyDict_SetItem(_dict, PyUnicode_FromString(_kv.first.c_str()), Py_BuildValue("b", _kv.second.boolean_value()));
                                }
                                else if(_kv.second.is_integer())
                                {
                                    PyDict_SetItem(_dict, PyUnicode_FromString(_kv.first.c_str()), Py_BuildValue("i", _kv.second.integer_value()));
                                }
                                else if(_kv.second.is_string())
                                {
                                    PyDict_SetItem(_dict, PyUnicode_FromString(_kv.first.c_str()), Py_BuildValue("s", _kv.second.string_value().c_str()));
                                }
                                else if(_kv.second.is_double())
                                {
                                    PyDict_SetItem(_dict, PyUnicode_FromString(_kv.first.c_str()), Py_BuildValue("d", _kv.second.double_value()));
                                }
                            }
                            PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_BuildValue("O", _dict));
                        }
                        else
                        {
                            PyDict_SetItem(dict, PyUnicode_FromString(kv.first.c_str()), Py_None);
                        }
                    }
                    PyObject *arglist = Py_BuildValue("(sOO)", collection, Py_None, dict);
                    PyObject *result = PyEval_CallObject(callback, arglist);

                    Py_DECREF(arglist);
                    Py_XDECREF(result);
                    Py_DECREF(callback);
                });
            } else {
                Py_DECREF(callback);
            }
        } else {
            Py_DECREF(callback);
        }
    });
#endif
}

void FirebaseFirestore::Set(const char* collection, const char* field, PyObject *value, PyObject *callback, bool timestamp)
{
	Future<void> firestoreFuture;
	std::string documentStr = std::string(collection) + "/" + GetImpl()->GetUserUID();
#if !defined(_WIN32)
	firebase::firestore::DocumentReference document_ref = Firestore::GetInstance()->Document(documentStr.c_str());
	if(PyDict_Check(value))
	{
		firebase::firestore::MapFieldValue mapFieldData;
        PyObject *key, *valueObject;
        Py_ssize_t pos = 0;

        while (PyDict_Next(value, &pos, &key, &valueObject)) {
            const char *parameter_name = PyUnicode_AsUTF8(key);
            if (PyBool_Check(valueObject)) {
                bool _value = PyLong_AsLong(valueObject);
                mapFieldData.insert({parameter_name, firebase::firestore::FieldValue::FromBoolean(_value)});
            }
            if (PyLong_Check(valueObject)) {
                int _value = (int)PyLong_AsLong(valueObject);
                mapFieldData.insert({parameter_name, firebase::firestore::FieldValue::FromInteger(_value)});
            } else if (PyFloat_Check(valueObject)) {
                double _value = PyFloat_AsDouble(valueObject);
                mapFieldData.insert({parameter_name, firebase::firestore::FieldValue::FromDouble(_value)});
            } else {
                const char *_value = PyUnicode_AsUTF8(valueObject);
                mapFieldData.insert({parameter_name, firebase::firestore::FieldValue::FromString(_value)});
            }
        }
        if(timestamp)
        {
            mapFieldData.insert({"timestamp", firebase::firestore::FieldValue::FromTimestamp(Timestamp::Now())});
        }
		firestoreFuture = document_ref.Set({ {field, firebase::firestore::FieldValue::FromMap(mapFieldData)} }, firebase::firestore::SetOptions::Merge());
	}
	else
	{
		firebase::firestore::FieldValue FieldData;
		if (PyBool_Check(value))
		{
			bool _value = PyLong_AsLong(value);
			FieldData = firebase::firestore::FieldValue::FromBoolean(_value);
		}
		else if (PyLong_Check(value))
		{
			int64_t _value = PyLong_AsLong(value);
			FieldData = firebase::firestore::FieldValue::FromInteger(_value);
		}
		else if (PyFloat_Check(value))
		{
			double _value = PyFloat_AsDouble(value);
			FieldData = firebase::firestore::FieldValue::FromDouble(_value);
		} else if(value != nullptr && value != Py_None) {
			const char* _value = PyUnicode_AsUTF8(value);
			FieldData = firebase::firestore::FieldValue::FromString(_value);
		}
        if(timestamp)
        {
            if(value != nullptr && value != Py_None)
            {
                firebase::firestore::MapFieldValue mapFieldData;
                mapFieldData.insert({"value", FieldData});
                mapFieldData.insert({"timestamp", firebase::firestore::FieldValue::FromInteger(Timestamp::Now().seconds())});
                firestoreFuture = document_ref.Set({ {field, firebase::firestore::FieldValue::FromMap(mapFieldData)} }, firebase::firestore::SetOptions::Merge());
            }
            else
            {
                FieldData = firebase::firestore::FieldValue::FromInteger(Timestamp::Now().seconds());
                firestoreFuture = document_ref.Set({ {field, FieldData} }, firebase::firestore::SetOptions::Merge());
            }
        }
        else
        {
            firestoreFuture = document_ref.Set({ {field, FieldData} }, firebase::firestore::SetOptions::Merge());
        }
	}

    if (!PyCallable_Check(callback))
    {
        return;
    }
    Py_INCREF(callback);
	firestoreFuture.OnCompletion([collection, field, callback, this](const Future<void>& future) {
		if (future.error() == firebase::firestore::kOk) {
            m_taskQueue.dispatch([collection, field, callback]() {
				PyObject* arglist = Py_BuildValue("(sss)", collection, field, "Successfully written");
				PyObject* result = PyEval_CallObject(callback, arglist);

				Py_DECREF(arglist);
				Py_XDECREF(result);
				Py_DECREF(callback);
			});
		}
		else {
            m_taskQueue.dispatch([collection, field, callback]() {
				PyObject* arglist = Py_BuildValue("(sss)", collection, field, "Error writing");
				PyObject* result = PyEval_CallObject(callback, arglist);

				Py_DECREF(arglist);
				Py_XDECREF(result);
				Py_DECREF(callback);
			});
		}
	});
#endif
}

void FirebaseFirestore::Delete(const char* collection, PyObject *callback)
{
    std::string documentStr = std::string(collection) + "/" + GetImpl()->GetUserUID();
#if !defined(_WIN32)
    firebase::firestore::DocumentReference document_ref = Firestore::GetInstance()->Document(documentStr.c_str());
    Future<void> firestoreFuture = document_ref.Delete();
    if (!PyCallable_Check(callback))
    {
        return;
    }
    Py_INCREF(callback);
    firestoreFuture.OnCompletion([collection, callback, this](const Future<void>& future) {
        if (future.error() == firebase::firestore::kOk) {
            m_taskQueue.dispatch([collection, callback]() {
                PyObject* arglist = Py_BuildValue("(sOs)", collection, Py_None, "Successfully deleted");
                PyObject* result = PyEval_CallObject(callback, arglist);

                Py_DECREF(arglist);
                Py_XDECREF(result);
                Py_DECREF(callback);
            });
        }
        else {
            m_taskQueue.dispatch([collection, callback]() {
                PyObject* arglist = Py_BuildValue("(ss)", collection, Py_None, "Error deleting");
                PyObject* result = PyEval_CallObject(callback, arglist);

                Py_DECREF(arglist);
                Py_XDECREF(result);
                Py_DECREF(callback);
            });
        }
    });
#endif
}

void FirebaseFirestore::Delete(const char* collection, const char* field, PyObject *callback)
{
    std::string documentStr = std::string(collection) + "/" + GetImpl()->GetUserUID();
#if !defined(_WIN32)
    firebase::firestore::DocumentReference document_ref = Firestore::GetInstance()->Document(documentStr.c_str());
    Future<void> firestoreFuture = document_ref.Update({{field, firebase::firestore::FieldValue::Delete()} });
    if (!PyCallable_Check(callback))
    {
        return;
    }
    Py_INCREF(callback);
    firestoreFuture.OnCompletion([collection, field, callback, this](const Future<void>& future) {
        if (future.error() == firebase::firestore::kOk) {
            m_taskQueue.dispatch([collection, field, callback]() {
                PyObject* arglist = Py_BuildValue("(sss)", collection, field, "Successfully deleted");
                PyObject* result = PyEval_CallObject(callback, arglist);

                Py_DECREF(arglist);
                Py_XDECREF(result);
                Py_DECREF(callback);
            });
        }
        else {
            m_taskQueue.dispatch([collection, field, callback]() {
                PyObject* arglist = Py_BuildValue("(sss)", collection, field, "Error deleting");
                PyObject* result = PyEval_CallObject(callback, arglist);

                Py_DECREF(arglist);
                Py_XDECREF(result);
                Py_DECREF(callback);
            });
        }
    });
#endif
}
