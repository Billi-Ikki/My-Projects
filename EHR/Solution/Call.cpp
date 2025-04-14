#include "Call.h"
#include<string>
#include<iostream>
using namespace std;
Call::Call()
{
	this->notes = "None";

}
Call::Call(Doctor D1)
{
	this->notes = "None";
	this->recordstatus = "Not Recorded";
	this->D = D1;
	time_t currentTime = time(nullptr);
	tm* localTime = localtime(&currentTime);
	currentYear = localTime->tm_year + 1900;
	currentMonth = localTime->tm_mon + 1;
	currentDay = localTime->tm_mday;
}
void Call::working()
{
	int choice = 0;
	system("cls");
	cout << "\t\t\t\t\tCalling!" << endl;
	while (choice != 1)
	{

		cout << "1 : End call!" << endl;
		cout << "2 : Record call " << endl;
		cout << "3 : Take Notes " << endl;
		cout << "Enter Your choice : ";
		cin >> choice;
		if (choice == 1)
		{
			system("cls");
			cout << "\t\t\t\t\tCall Ended!" << endl;
		}
		else if (choice == 2)
		{
			system("cls");
			cout << "\t\t\t\t\tYour call is being Recorded" << endl;
			this->recordstatus = "Recored";
		}
		else if (choice == 3)
		{
			cout << "Enter your notes : ";
			cin.ignore();
			getline(cin, this->notes);
			system("cls");
			cout << "\t\t\t\t\tNotes saved Successfully ! " << endl;
		}
		else
		{
			cout << "Invalid Choice!" << endl;
		}
	}
}
void Call::display()
{
	cout << "Doctor Name  :  " << D.getName() << endl;
	cout << "Doctor ID    :  " << D.getID() << endl;
	cout << "Call Date    :  " << this->currentDay << "/" << this->currentMonth << "/" << this->currentYear << endl;
	cout << "Call Status  :  " << this->recordstatus << endl;
	cout << "Notes        :  " << this->notes << endl;
}