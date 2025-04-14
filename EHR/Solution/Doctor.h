#pragma once
#include <iostream>
using namespace std;
class Doctor
{
private:
    string name;
    string specialization;
    string id;
    string password;
    //Patient P;
    int index;
public:
   
    
    Doctor(string name, string spec, string id, string password,int index);
    Doctor();
    void DisplayAll();
    // Getter functions
    string getName() const 
    {
        return name;
    }
    string getSpecialization() const 
    {
        return specialization;
    }
    string getID() const 
    {
        return id;
    }
    string getPassword() const 
    {
        return password; 
    }
    int getIndex() const 
    {
        return index; 
    }

    // Setter functions
    void setName(const string& newName) 
    {
        name = newName;
    }
    void setSpecialization(const string& newSpecialization) 
    {
        specialization = newSpecialization; 
    }
    void setID(const string& newID)
    {
        id = newID; 
    }
    void setPassword(const string& newPassword)
    {
        password = newPassword; 
    }
    void setIndex(int newIndex) 
    {
        index = newIndex; 
    }

};

