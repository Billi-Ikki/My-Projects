#include "PatientApp.h"
#include<fstream>
void InsertobjectR(RMC object)
{
	ofstream myFile("Cloud.dat", ios::binary | ios::out);
	if (myFile.write((char*)&object, sizeof(object)))
		cout << "\n";
	else
		cout << "Object Insertion Failed" << endl;
	myFile.close();
}
PatientApp::PatientApp(Patient* p, EHR* e, iotsensors* i, Appointment* a, Call* c, Doctor* d)
{
	this->P = p;
	this->E = e;
	this->I = i;
	this->A = a;
	this->C = c;
	this->D = d;
	this->index = 0;
}
void PatientApp::P_Encryption(Patient P1)
{
	int i = 0;
	i = P1.getIndex();
	int j = 0;
	string encrypt;
	int encryp;
	encrypt = P[i].getID();
	while (encrypt[j] != '\0')
	{
		encrypt[j] += '2';
		j++;
	}
	j = 0;
	P[i].setID(encrypt);
	encryp = P[i].getAge();
	encryp = encryp << 2;
	P[i].setAge(encryp);
	j = 0;
	encrypt = P[i].getPassword();
	while (encrypt[j] != '\0')
	{
		encrypt[j] += '2';
		j++;
	}
	j = 0;
	P[i].setPassword(encrypt);
}
void PatientApp::E_Encrypt(EHR E1, int i)//i is index
{
	string encryption;
	encryption = E[i].getAllergies();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setAllergies(encryption);

	encryption = E[i].getChronicHealthCondition();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setChronicHealthCondition(encryption);
	encryption = E[i].getConsultations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setConsultations(encryption);
	encryption = E[i].getDietaryRestriction();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setDietaryRestriction(encryption);
	encryption = E[i].getPrescriptions();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setPrescriptions(encryption);


	encryption = E[i].getRecommendations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setRecommendations(encryption);
	encryption = E[i].getRegularMedication();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] += '2';
	}
	E[i].setRegularMedication(encryption);
}
void PatientApp::I_Encrypt(iotsensors I1, int i)
{
	int size = 0;
	int encryp = 0;
	encryp = I[i].getDay();
	encryp = encryp << 2;
	I[i].setDay(encryp);
	encryp = I[i].getMonth();
	encryp = encryp << 2;
	I[i].setMonth(encryp);
	encryp = I[i].getYear();
	encryp = encryp << 2;
	I[i].setYear(encryp);
	size = I[i].getSize();
	int* encryption;
	encryption = new int[size];
	for (int j = 0; j < size; j++)
	{
		encryption = I[i].getBmi();
		encryption[j] = encryption[j] << 2;
		I[i].setBmi(encryption);
		encryption = I[i].getOxygenSaturation();
		encryption[j] = encryption[j] << 2;
		I[i].setOxygenSaturation(encryption);
		encryption = I[i].getPulse();
		encryption[j] = encryption[j] << 2;
		I[i].setPulse(encryption);
		encryption = I[i].getBloodPressure();
		encryption[j] = encryption[j] << 2;
		I[i].setBloodPressure(encryption);
		encryption = I[i].getHandTremor();
		encryption[j] = encryption[j] << 2;
		I[i].setHandTremor(encryption);
		encryption = I[i].getGeneralMovement();
		encryption[j] = encryption[j] << 2;
		I[i].setGeneralMovement(encryption);
	}
}
void PatientApp::C_Encrypt(Call C1, int i)
{
	int incrypt;
	string encrypt;
	int j = 0;
	encrypt = C[i].getNotes();
	while (encrypt[j] != '\0')
	{
		encrypt[j] += '2';
		j++;
	}
	C[i].setNotes(encrypt);
	j = 0;
	encrypt = C[i].getRecordStatus();
	while (encrypt[j] != '\0')
	{
		encrypt[j] += '2';
		j++;
	}
	C[i].setRecordStatus(encrypt);
	j = 0;
	incrypt = C[i].getCurrentDay();
	incrypt = incrypt << 2;
	C[i].setCurrentDay(incrypt);

	incrypt = C[i].getCurrentMonth();
	incrypt = incrypt << 2;
	C[i].setCurrentMonth(incrypt);

	incrypt = C[i].getCurrentYear();
	incrypt = incrypt << 2;
	C[i].setCurrentYear(incrypt);
}
void PatientApp::A_Encrypt(Appointment A1, int i)
{
	string encrypt = A[i].getStatus();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] += '2';
	}
	A[i].setStatus(encrypt);
	encrypt = A[i].getRTime();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] += '2';
	}
	A[i].setRTime(encrypt);
	int incrypt;
	incrypt = A[i].getRHour();
	incrypt = incrypt << 2;
	A[i].setRHour(incrypt);
	incrypt = A[i].getRMinute();
	incrypt = incrypt << 2;
	A[i].setRMinute(incrypt);
}
void PatientApp::P_Decryption(Patient P1)
{
	int i = 0;
	i = P1.getIndex();
	int j = 0;
	string encrypt;
	int encryp;
	encrypt = P[i].getID();
	while (encrypt[j] != '\0')
	{
		encrypt[j] -= '2';
		j++;
	}
	j = 0;
	P[i].setID(encrypt);
	encryp = P[i].getAge();
	encryp = encryp >> 2;
	P[i].setAge(encryp);
	j = 0;
	encrypt = P[i].getPassword();
	while (encrypt[j] != '\0')
	{
		encrypt[j] -= '2';
		j++;
	}
	j = 0;
	P[i].setPassword(encrypt);
}
void PatientApp::E_Decrypt(EHR E1, int i)//i is index
{
	string encryption;
	encryption = E[i].getAllergies();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setAllergies(encryption);

	encryption = E[i].getChronicHealthCondition();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setChronicHealthCondition(encryption);
	encryption = E[i].getConsultations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setConsultations(encryption);
	encryption = E[i].getDietaryRestriction();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setDietaryRestriction(encryption);
	encryption = E[i].getPrescriptions();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setPrescriptions(encryption);


	encryption = E[i].getRecommendations();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setRecommendations(encryption);
	encryption = E[i].getRegularMedication();
	for (int x = 0; encryption[x] != '\0'; x++)
	{
		encryption[x] -= '2';
	}
	E[i].setRegularMedication(encryption);
}
void PatientApp::I_Decrypt(iotsensors I1, int i)
{
	int size = 0;
	int encryp = 0;
	encryp = I[i].getDay();
	encryp = encryp >> 2;
	I[i].setDay(encryp);
	encryp = I[i].getMonth();
	encryp = encryp >> 2;
	I[i].setMonth(encryp);
	encryp = I[i].getYear();
	encryp = encryp >> 2;
	I[i].setYear(encryp);
	size = I[i].getSize();
	int* encryption;
	encryption = new int[size];
	for (int j = 0; j < size; j++)
	{
		encryption = I[i].getBmi();
		encryption[j] = encryption[j] >> 2;
		I[i].setBmi(encryption);
		encryption = I[i].getOxygenSaturation();
		encryption[j] = encryption[j] >> 2;
		I[i].setOxygenSaturation(encryption);
		encryption = I[i].getPulse();
		encryption[j] = encryption[j] >> 2;
		I[i].setPulse(encryption);
		encryption = I[i].getBloodPressure();
		encryption[j] = encryption[j] >> 2;
		I[i].setBloodPressure(encryption);
		encryption = I[i].getHandTremor();
		encryption[j] = encryption[j] >> 2;
		I[i].setHandTremor(encryption);
		encryption = I[i].getGeneralMovement();
		encryption[j] = encryption[j] >> 2;
		I[i].setGeneralMovement(encryption);
	}
}
void PatientApp::C_Decrypt(Call C1, int i)
{
	int incrypt;
	string encrypt;
	int j = 0;
	encrypt = C[i].getNotes();
	while (encrypt[j] != '\0')
	{
		encrypt[j] -= '2';
		j++;
	}
	C[i].setNotes(encrypt);
	j = 0;
	encrypt = C[i].getRecordStatus();
	while (encrypt[j] != '\0')
	{
		encrypt[j] -= '2';
		j++;
	}
	C[i].setRecordStatus(encrypt);
	j = 0;
	incrypt = C[i].getCurrentDay();
	incrypt = incrypt >> 2;
	C[i].setCurrentDay(incrypt);

	incrypt = C[i].getCurrentMonth();
	incrypt = incrypt >> 2;
	C[i].setCurrentMonth(incrypt);

	incrypt = C[i].getCurrentYear();
	incrypt = incrypt >> 2;
	C[i].setCurrentYear(incrypt);
}
void PatientApp::A_Decrypt(Appointment A1, int i)
{
	string encrypt = A[i].getStatus();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] -= '2';
	}
	A[i].setStatus(encrypt);
	encrypt = A[i].getRTime();
	for (int j = 0; encrypt[j] != '\0'; j++)
	{
		encrypt[j] -= '2';
	}
	A[i].setRTime(encrypt);
	int incrypt;
	incrypt = A[i].getRHour();
	incrypt = incrypt >> 2;
	A[i].setRHour(incrypt);
	incrypt = A[i].getRMinute();
	incrypt = incrypt >> 2;
	A[i].setRMinute(incrypt);
}
void PatientApp::Encryptions(int index, int doc_index, int iD, int iP)
{
	this->index = index;
	for (int i = 0; i < iP; i++)
	{
		P_Encryption(P[i]);
		E_Encrypt(E[i], i);
		I_Encrypt(I[i], i);
		C_Encrypt(C[i], i);
	}
	for (int i = 0; i < iD; i++)
	{
		A_Encrypt(A[i], i);
	}
}
void PatientApp::Decryptions(int index, int doc_index, int iD, int iP)
{
	this->index = index;
	for (int i = 0; i < iP; i++)
	{
		P_Decryption(P[i]);
		E_Decrypt(E[i], i);
		I_Decrypt(I[i], i);
		C_Decrypt(C[i], i);
	}
	for (int i = 0; i < iD; i++)
	{
		A_Decrypt(A[i], i);
	}
}
void PatientApp::working(int index, int doc_index, int iD, int iP, Patient* p, EHR* e, iotsensors* i, Appointment* a, Call* c, Doctor* d)
{
	this->R = RMC(E, I, A, C);
	int choice4 = 0;
	int choice = 0;
	int check = 1;
	int x = 0, choice2 = 0;
	string specialization, name, id, choice3;
	while (choice2 != 4)
	{
		cout << "\n1 : Make an Appointment " << endl;
		cout << "2 : Call the Doctor " << endl;
		cout << "3 : Proceed " << endl;
		cout << "4 : Exit " << endl;
		cin >> choice2;
		if (choice2 == 1)
		{
			cout << "Enter Doctor specialization you are loking for : ";
			cin >> specialization;
			cout << "\nAvailable doctors according to your mentioned specialization are\n ";
			for (int i = 0; i < 5; i++)
			{
				if (D[i].getSpecialization() == specialization)
				{
					D[i].DisplayAll();
				}
			}
			cout << "\nEnter the Id of doctor you want to choose : ";
			cin >> choice3;
			cout << "Avaliable appointments : \n\n";

			for (int i = 0; i < iD; i++)
			{
				if (choice3 == D[i].getID())
				{
					x = i;
				}
			}
			A[x].appointmentlist(P[index]);
		}
		else if (choice2 == 2)
		{
			cout << "Enter your Doctor Name : ";
			cin >> name;
			cout << "Enter your Doctor ID : ";
			cin >> id;
			for (int i = 0; i < 10; i++)
			{
				if (D[i].getName() == name)
				{
					if (D[i].getID() == id)
					{
						C[index] = Call(D[i]);
						C[index].working();
					}

				}
			}
		}
		else if (choice2 == 3)
		{
			PatientApp P_App(P, E, I, A, C, D);
			choice = 0;
			if(check==1)
			P_App.Encryptions(index, x, iD, iP);
			this->R = RMC(E, I, A, C);
			check++;
			cout << endl;
			InsertobjectR(R);
			system("cls");
			cout << "1  :  View Data\n";
			cout << "2  :  Exit\n";
			cout << "Enter your choice  : ";
			cin >> choice;
			//choice4 == 0;
			if (choice == 1)
			{
				choice4 = 0;
				while (choice4 != 5)
				{
					cout << "\n1 : call data\n";
					cout << "2 : Appointment data\n";
					cout << "3 : EHR\n";
					cout << "4 : IOT Data\n";
					cout << "5 : Exit\n";
					cin >> choice4;
					if (choice4 == 1)
					{
						system("cls");
						cout << "\t\t\t\t\tCall Data\n";
						R.reterivedatacall(index);
						//C[index].display();
					}
					else if (choice4 == 2)
					{
						system("cls");
						cout << "\t\t\t\t\tAppointment Data\n";
						R.reteriveAppointment(x);
					}
					else if (choice4 == 3)
					{
						system("cls");
						cout << "\t\t\t\t\tEHR Data\n";
						R.reterivedataEhr(index);
					}
					else if (choice4 == 4)
					{
						system("cls");
						cout << "\t\t\t\t\tIOT Sensors Data\n";
						R.reteriveiotData(index);
					}
					else if (choice4 == 5)
					{
						system("cls");
						cout << "\t\t\t\t\t  Exiting\n";
						//P_App.Decryptions(index, x, iD, iP);
						cout << "\n";
					}
					else
					{
						cout << "Invalid choice!" << endl;
					}
				}
			}
			else
			{
				choice2 = 4;
			}
		}
		else if (choice2 == 4)
		{
			//this->index = index;
			/*for (int i = 0; i < iP; i++)
			{
				P_Encryption(P[i]);
				E_Encrypt(E[i], i);
				I_Encrypt(I[i], i);
				C_Encrypt(C[i], i);
			}
			for (int i = 0; i < iD; i++)
			{
				A_Encrypt(A[i], i);
			}*/
			//this->Encryptions(index,x,iD,iP);
			for (int j = 0; j < iP; j++)
			{
				P_Decryption(p[j]);
				E_Decrypt(e[j], j);
				I_Decrypt(i[j], j);
				C_Decrypt(c[j], j);
			}
			for (int i = 0; i < iD; i++)
			{
				A_Decrypt(a[i], i);
			}
			cout << "\t\t\t\t\t  Exiting\n";
		}
		else
		{
			cout << "Invalid input\n";
		}
	}
}