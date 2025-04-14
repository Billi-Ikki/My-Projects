#include "Patient.h"
Patient::Patient()
{
        this->name = "\0";
        this->index = 0;
        this->id = "\0";
        this->password = "\0";
        this->index = 0;
}
Patient::Patient(string name, string id, string password, int age , int index)
{
    this->name = name;
    this->id = id;
    this->password = password;
    this->age = age;
    this->index = index;
}
void Patient::DisplayAll()
{
    cout << "Name   : " << this->name << endl;
    cout << "ID     : " << this->id << endl;
    cout << "Age    : " << this->age << endl;
   // cout << "Password : " << this->password << endl;
}