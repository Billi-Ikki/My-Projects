#include "Doctor.h"
Doctor::Doctor(string name, string spec, string id, string password, int index)
{
    this->name = name;
    this->specialization = spec;
    this->id = id;
    this->password = password;
    this->index = index;
}
Doctor::Doctor()
{
    this->name = "\0";
    this->specialization = "\0";
    this->id = "\0";
    this->password = "\0";
}
void Doctor::DisplayAll()
{
    cout << "\n\nName : " << this->name << endl;
    cout << "Id   : " << this->id << endl;
   // cout << "Password : " << this->password << endl;
    cout << "Specialization  : " << this->specialization << endl;
}