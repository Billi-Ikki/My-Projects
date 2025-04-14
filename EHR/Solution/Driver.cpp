#include"PatientApp.h"
#include<iostream>
#include<fstream>
#include<string>
void InsertobjectP(Patient object)
{
	int i = 0;
	string name = object.getName();
	ofstream myFile(name+"P.dat", ios::binary | ios::out);
	if (myFile.write((char*)&object, sizeof(object)))
		cout << " ";
	else
		cout << "Object Insertion Failed" << endl;
	myFile.close();
}
void InsertobjectD(Doctor object)
{
	int i = 0;
	string name = object.getName();
	ofstream myFile(name+"D.dat", ios::binary | ios::out);
	if (myFile.write((char*)&object, sizeof(object)))
		cout << " ";
	else
		cout << "Object Insertion Failed" << endl;
	myFile.close();
}
using namespace std;
int main()
{
	int x = 0;
	string choice3;
	int check = 0;
	int iP = 10;
	int iD = 5;
	int choice = 0;
	int age = 18;
	int index = 0;
	int doctorindex = 0;
	int choice2 = 0;
	PatientApp PP;
	string name, id, specialization, password;
	Patient* P;
	P = new Patient[20];
	P[0] = Patient("Bilal", "1", "12345", 18, 0);
	P[1] = Patient("Umer", "2", "12345", 25, 1);
	P[2] = Patient("Hassan", "3", "12345", 12, 2);
	P[3] = Patient("Mirza", "4", "12345", 43, 3);
	P[4] = Patient("Saif", "5", "12345", 12, 4);
	P[5] = Patient("Ali", "6", "12345", 34, 5);
	P[6] = Patient("Ahmad", "7", "12345", 56, 6);
	P[7] = Patient("Saad", "8", "12345", 23, 7);
	P[8] = Patient("Muhaiman", "9", "12345", 16, 8);
	P[9] = Patient("Munni", "10", "12345", 19, 9);

	Doctor* D = new Doctor[10];
	D[0] = Doctor("Touseef", "Endocrinology", "1", "12345", 0);
	D[1] = Doctor("Zaim", "Oncology", "2", "12345", 1);
	D[2] = Doctor("Ali Hassan", "Cardiology", "3", "12345", 2);
	D[3] = Doctor("Ubaida", "Cardiology", "4", "12345", 3);
	D[4] = Doctor("Zubair", " Psychology", "5", "12345", 4);

	iotsensors* I;
	I = new iotsensors[20];
	for (int i = 0; i < iP; i++)
	{
		I[i] = iotsensors(P[i]);
	}
	EHR* E;
	E = new EHR[20];
	for (int i = 0; i < iP; i++)
	{
		E[i] = EHR(P[i]);
	}
	Appointment* A;
	A = new Appointment[10];
	for (int i = 0; i < iD; i++)
	{
		A[i] = Appointment(D[i]);
	}
	Call* C;
	C = new Call[20];
	for (int i = 0; i < iP; i++)
	{
		C[i] = Call(D[0]);
	}
	for (int i = 0; i < 10; i++)
	{
		InsertobjectP(P[i]);
	}
	for (int i = 0; i < 5; i++)
	{
		InsertobjectD(D[i]);
	}
	cout << "\n\t\t\t\tWelcome to Pak Remote Health Monitoring system\n";
	while (choice != 5)
	{
		cout << "1  :  Patient\n2  :  Doctor\n3  :  Register as Patient\n4  :  Register as Doctor\n5  :  Exit\n";
		cout << "Enter your Choice : ";
		cin >> choice;

		if (choice == 1)
		{
			cin.ignore();
			cout << "Enter Your name : ";
			getline(cin, name);
			cout << "Enter Your Id : ";
			cin >> id;
			for (int i = 0; i < 20; i++)
			{
				if (P[i].getName() == name)
				{
					if (P[i].getID() == id)
					{
						cout << "Enter Your Password : ";
						cin >> password;
						if (P[i].getPassword() == password)
						{
							system("cls");
							cout << "\n\t\t\t\t\tWelcome!\n\n";
							index = P[i].getIndex();
							check = 1;

						}
						else
						{
							cout << "Invalid Data try Again ! \n";
						}

					}
					else
					{
						system("cls");
						cout << "Invalid Data Try again!!" << endl;
					}
				}
			}
		}
		else if (choice == 2)
		{
			cin.ignore();
			cout << "Enter Your name : ";
			getline(cin, name);
			cout << "Enter Your Id : ";
			cin >> id;
			for (int i = 0; i < 10; i++)
			{
				if (D[i].getName() == name)
				{
					if (D[i].getID() == id)
					{
						cout << "Enter Your Password : ";
						cin >> password;
						if (D[i].getPassword() == password)
						{
							system("cls");
							cout << "\n\t\t\t\t\tWelcome!\n\n";
							doctorindex = D[i].getIndex();
							check = 2;
						}
						else
						{
							cout << "Invalid Data!\n";
						}

					}
					else
					{
						system("cls");
						cout << "Invalid Data!\n" << endl;
					}
				}

			}
		}
		else if (choice == 3)
		{
			check = 0;
			cin.ignore();
			cout << "Enter your name : ";
			getline(cin, name);
			cout << "Enter your id : ";
			cin >> id;
			cout << "Enter your age : ";
			cin >> age;
			cout << "Enter your password : ";
			cin >> password;
			P[iP] = Patient(name, id, password, age, iP);
			InsertobjectP(P[iP]);
			I[iP] = iotsensors(P[iP]);
			E[iP] = EHR(P[iP]);
			cout << "Record Added Successfully \n";
			iP++;
		}
		else if (choice == 4)
		{
			check = 0;
			cout << "Enter your name : ";
			cin >> name;
			cout << "Enter your id : ";
			cin >> id;
			cout << "Enter your specialization : ";
			cin >> specialization;
			cout << "Enter your password : ";
			cin >> password;
			D[iD] = Doctor(name, specialization, id, password, iD);
			InsertobjectD(D[iD]);
			A[iD] = Appointment(D[iD]);
			cout << "Record added Successfully " << endl;
			iD++;
		}
		else if (choice == 5)
		{
			cout << "\t\t\tThanks for visiting " << endl;
			check = 0;
		}
		else
		{
			cout << "Invalid Choice!";
			check = 0;
		}

		if (check == 1)
		{
			PatientApp App(P, E, I, A, C, D);
			App.working(index, doctorindex, iD, iP, P, E, I, A, C, D);
			/*App.Decryptions(index, doctorindex, iD, iP);
			App.Encryptions(index, x, iD, iP);*/
		}
		else if (check == 2)
		{
			/*PatientApp App(P, E, I, A, C, D);
			App.Encryptions(index, x, iD, iP);*/
			//C[0].display();
			//DoctorApp D(int docindex, int);
			RMC R(E, I, A, C);
			DoctorApp Dapp(P, I, R, D,A, index, doctorindex, iD, iP);
			Dapp.working(iD, iP);
		}
	}
}
