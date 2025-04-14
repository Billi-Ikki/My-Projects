#include "DoctorApp.h"
#include<string>
#include<iostream>
using namespace std;
DoctorApp::DoctorApp()
{
	this->patientindex = 0;
	this->docindex = 0;

}
DoctorApp::DoctorApp(Patient* P, iotsensors* I, RMC R, Doctor* D, Appointment* A, int patient_index, int doc_index, int iD, int iP)
{
	this->p = P;
	this->i = I;
	this->r = R;
	this->d = D;
	this->a = A;
	this->patientindex = patient_index;
	this->docindex = doc_index;
}
void DoctorApp::working(int iD, int iP)
{
	int access = 0;
	int choice = 0;
	int c2 = 0;
	int choice2 = 0;
	string name;
	string id;
	string pass;
	int pindex = 0;
	string add;
	while (choice != 7)
	{
		cout << "1 : View (and approve or reject) appiontment requests " << endl;
		cout << "2 : View past consultation of any patient " << endl;
		cout << "3 : Search for particular data of any of their patients" << endl;
		cout << "4 : Request access to additional data " << endl;
		cout << "5 : Add data into a patient’s medical record" << endl;
		cout << "6 : Edit patient EHR" << endl;
		cout << "7 : Exit" << endl;
		cout << "Enter Your choice : " << endl;
		cin >> choice;
		system("cls");
		if (choice == 1)
		{
			cout << "\t\t\t\t\tAPPOINTMENT REQUESTS \n";
			a[docindex].appointmentrequests();
			cout << "\n1 : Approve \n2 : Disaprove\n";
			cin >> c2;
			if (c2 == 1)
			{
				a[docindex].setStatus("Approved");
			}
			else
			{
				a[docindex].setStatus("DisApproved");
			}
		}
		else if (choice == 2)
		{
			cout << "Enter the id of Patient : ";
			cin >> id;
			for (int j = 0; j < iP; j++)
			{
				if (p[j].getID() == id)
				{
					r.consultationsdata(j);

				}
			}
		}
		else if (choice == 3)
		{
			cout << "Enter the id of Patient : ";
			cin >> id;
			for (int j = 0; j < iP; j++)
			{
				if (p[j].getID() == id)
				{
					pindex = j;
				}
			}
			cout << "\n1 : IOT \n";
			cout << "2 : Personal Details\n";
			cout << "3 : EHR\n";
			cin >> choice2;
			if (choice2 == 1)
			{
				i[pindex].Displayall();
			}
			else if (choice2 == 2)
			{
				p[pindex].DisplayAll();
			}
			else
			{
				r.EHRdataDA(pindex);
			}
		}
		else if (choice == 4)
		{
			cout << "Authenticate Yourself ";
			cin >> pass;
			if (pass == d[pindex].getPassword())
			{
				if (rand() % 100 > 10 )
				{
					cout << "Request Granted!" << endl;
					access = 1;
				}
				else
				{
					cout << "Request Declined! " << endl;
					access = -1;
				}
			}
			else
			{
				cout << "Invalid Password!" << endl;
			}
		}
		else if (choice == 5)
		{
			if (access == 1)
			{
				cout << "Enter Patient iD : ";
				cin >> id;
				for (int j = 0; j < iP; j++)
				{
					if (p[j].getID() == id)
					{
						pindex = j;
					}
				}
				r.ehr(pindex);
			}
			else
			{
				cout << "Permission not Allowed \n";
			}
		}
		else if (choice == 6)
		{
			cout << "Enter Patient iD which you want to edit : ";
			cin >> id;
			for (int j = 0; j < iP; j++)
			{
				if (p[j].getID() == id)
				{
					pindex = j;
				}
			}
			cout << "What do you want to edit ?\n";
			cout << "1 : consultation \n2 : prescriptions\n3 : Recommendations\n4 : DietaryRestriction\n5 : Allergies\n6 :  RegularMedication\n7 : ChronicHealthCondition\n";
			cout << "Enter your choice : ";
			cin >> choice2;
			if (choice2 == 1)
			{
				cout << "Enter new consultations ";
				cin.ignore();
				getline(cin, add);
				r.updateObject(pindex, add, choice2);
			}
			else if (choice2 == 2)
			{
				cout << "Enter new Prescriptions ";
				cin.ignore();
				getline(cin, add);
				r.updateObject(pindex, add, choice2);
			}
			else if (choice2 == 3)
			{
				cout << "Enter new Recomendations ";
				cin.ignore();
				getline(cin, add);
				r.updateObject(pindex, add, choice2);
			}
			else if (choice2 == 4)
			{
				cout << "Enter new Dietry Restrictions ";
				cin.ignore();
				getline(cin, add);
				r.updateObject(pindex, add, choice2);
			}
			else if (choice2 == 5)
			{
				cout << "Enter new Allergies ";
				cin.ignore();
				getline(cin, add);
				r.updateObject(pindex, add, choice2);
				cout << "Updated Sucessfully" << endl;
			}
			else if (choice2 == 6)
			{
				cout << "Enter new Regular Medication ";
				cin.ignore();
				getline(cin, add);
				r.updateObject(pindex, add, choice2);
			}
			else if (choice2 == 7)
			{
				cout << "Enter new Chronic Health Condition ";
				cin.ignore();
				getline(cin, add);
				r.updateObject(pindex, add, choice2);
			}
			else
			{
				cout << "Invalid Choice !" << endl;
			}
		}
		else if (choice == 7)
		{
			cout << "       Good Bye :)      " << endl;
		}
		else
		{
			cout << "INVALID CHOICE!" << endl;
		}

	}
}