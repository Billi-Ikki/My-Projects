#pragma once
#include"Doctor.h"
#include<iostream>
using namespace std;
class Patient
{
private:
	string name;
	string id;
	string password;
    Doctor D;
	int age;
	int index;
public:
    Patient();
    Patient(string name, string id, string password, int age, int index);
    void DisplayAll();
    // Getter functions
    string getName() const 
    {
        return name;
    }
    string getID() const 
    {
        return id; 
    }
    string getPassword() const 
    { 
        return password;
    }
    int getAge() const
    {
        return age;
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
    void setID(const string& newID)
    {
        id = newID; 
    }
    void setPassword(const string& newPassword)
    {
        password = newPassword; 
    }
    void setAge(int newAge)
    {
        age = newAge;
    }
    void setIndex(int newIndex) 
    {
        index = newIndex; 
    }
};

