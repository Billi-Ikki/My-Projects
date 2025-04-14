/* Name : Muhammad Bilal Ikram
   Section : BS-CY_A
   Roll No  : 22i-1636
   Programming Fundamentals Final Project
   */
#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include <cstdlib>
#include <ctime>

using namespace std;

// Function prototypes
void readData(string[][3], int , float[]);

void updateData(float[],float [],float [], int);

void showMarketScreen(string[][3],float[],float[],float[],float[],int,string,string,int);

void showPortfolioScreen(string[][3],float[],float[],float[],float[],int[],float[],int,int[],string);


int main()
{
	int share=0,totalshares=0;
	
	srand(time(0));

	// Declare and initialize the 2D array
	
	const int rows = 37;
	
	float CP[rows]={},PP[rows]={}, checkperci[rows], checkpercd[rows], shares[rows],percchange[rows];
	
	int gain_loss[rows], accountbalance[rows], amount=0;

	float High[rows], min = percchange[0], max = percchange[0], Low[rows];
	
	string symbol[rows];

	string stocks[rows][3] = {};
	
	string search,name,topadvancer,topdecliner;
	
	char ch,choice;
	
	ofstream fout; 
	
	accountbalance[0]=10000;
	
	// CALLING TO FUNCTION TO READ DATA FROM COMPANIES.txt file
	
	readData(stocks,rows,CP);
	
	//LOOP TO Find highest and lowest value that increase or decrease in one session
	
	for(int i=0; i<rows; i++)

	   {
	   
	   symbol[i]=stocks[i][0];
	   
	   shares[i]=rand()%50;
	   
	   checkperci[i]=0.15*CP[i];
	   
	   checkperci[i]=CP[i]+checkperci[i];
	   
	   checkpercd[i]=0.15*CP[i];
	   
	   checkpercd[i]=CP[i]-checkpercd[i];
	   
	   High[i]=CP[i];
	   
	   Low[i]=CP[i];
	   
	   
	    }
	
	// Loop to display Market for the first time

	while(ch!='E')
	
	{
	
	// Call the readData function

	readData(stocks,rows,CP);
	
	// To keep record of previous Data

	for(int i=0; i<rows; i++)

	   {
	    totalshares=totalshares+shares[i];
	    PP[i]=CP[i];

	    }

	
	// Call the updateData function

	updateData(CP,checkperci,checkpercd, rows);
	
	  for(int i=0; i<rows; i++)
 	 
 	 {
 	 
 	 // Max is used to find top advancer
 	 
 	 max = percchange[0]; 
	
	//min is used toa find out top decliner
	
	 min = percchange[0]; 
 	 
 	 
 	  if(High[i]<CP[i])
 	 
 	  {
 	 
 	  High[i]=CP[i];
 	 
 	  }
  	 
  	 if(Low[i]>CP[i])
  	 
  	 {
  	 
  	 Low[i]=CP[i];
  	 
  	 }
  	 
  	 // Perc Change is used to calculate total percentage change to help finding out Advancer and Decliner
  	 
  	 percchange[i]=((CP[i]-PP[i])/PP[i])*100;
  	 
  	     
  
         for (int i = 0; i < rows ; i++) 
        
         {
        
         if (percchange[i] > max) 
         
         {
         
         max = percchange[i]; 
  	 
  	 topadvancer=symbol[i];
  	 
  	 }
  	 
  	 if (percchange[i] < min) 
         
         {
         
         min = percchange[i]; 
  	 
  	 topdecliner=symbol[i];
  	 
  	 }
  	 
  	 }
  	 
  	 // Calculating Gain or Loss
  	 
  	 gain_loss[i]=(CP[i]-PP[i])*shares[i];
  	 
  	 }
	
	
	// Call the showMarketScreen function
	
	system("clear");
	
	showMarketScreen(stocks,CP,PP,High,Low,rows,topadvancer,topdecliner,totalshares);
	
	// Writing Updated data on companies.txt file
	
	fout.open("companies.txt");
	
	for(int i=0; i<rows; i++)
   	
   	  {
        
        fout << stocks[i][0] << "," << stocks[i][1] << "," << CP[i] ;
    	
    	 }
    	
    	fout.close();
	
	cout << "Enter your choice \n";
			
	cin.get(ch);
	
	// MENU
	
	if (ch == 'P')
	
	{
	
	cin.ignore();
	
	cout << "Enter Your Name : ";
	
	getline(cin,name);
	
	cout << "Enter the amount of money which you want to include in your account balance : ";
	
	cin >> accountbalance[0];
	
	while(accountbalance[0] <0)
	
		cin >> accountbalance[0];
	
	// Show Portfolioscreen
	
	while(choice!='E')
	
		{
	
		showPortfolioScreen(stocks,CP,PP,High,Low,gain_loss,shares,rows,accountbalance,name);
	
		// Call the readData function

		readData(stocks,rows,CP);
	
		// To keep record of previous Data

		for(int i=0; i<rows; i++)

		   {

		    PP[i]=CP[i];

		    }

	
		// Call the updateData function

		updateData(CP,checkperci,checkpercd, rows);
	
		  for(int i=0; i<rows; i++)
 	 
		 	 {
 	 
		 	  if(High[i]<CP[i])
 	 
		 	  {
 	 
		 	  High[i]=CP[i];
 	 
		 	  }
  	 
		  	 if(Low[i]>CP[i])
  	 
		  	 {
  	 
		  	 Low[i]=CP[i];
	  	 
		  	 }
  	 
	  		 percchange[i]=((CP[i]-PP[i])/PP[i])*100;
  	 
  	 
  	 	
	  		 gain_loss[i]=(CP[i]-PP[i])*shares[i];
  	 
	  	 }
	
		//Write Updated Data
	
		fout.open("companies.txt");
	
		for(int i=0; i<rows; i++)
   	
		   	  {
        
		        fout<<stocks[i][0]<<","<<stocks[i][1]<<","<<CP[i];
    	
		    	 }
    	
	    	fout.close();
	
		cin.get(choice);
	
		//MENU FOR PORTFOLIO
	
		if (choice == 'L')
		
		{
		
		break;
		
		}
		
		if(choice=='A')
		{
		
		cout << "Enter the symbol of the company of which you want to buy the stock : ";
		
		cin >> search;

		for(int i=0; i<=rows; i++)
		
		{
		
			if(symbol[i]==search)
			{
		
			cout << "Enter how many shares you want to buy : ";
		
			cin >> shares[i];
			
			
			if(shares[i]>accountbalance[0])
			{
		
			cout << "Your account balance is not enough enter shares according to your account balance : ";
		
			cin >> shares[i]; 
		
			}
		
			accountbalance[0]=accountbalance[0]-shares[i];
			break;
			}
			
		    }
		
		}
		
		
		 if(choice =='R')
		
		{
		
		cout << "Enter the symbol of the company of which you want to sale the stock : ";
		
		cin >> search;

		for(int i=0; i<=rows; i++)
		
		{
		
			if(symbol[i]==search)
			{
		
			cout << "Enter how many shares you want to sale : ";
			
			cin >> share;
		
			if(share>shares[i])
			{
		
			cout << "You dont have much shares to sell Enter valid share : ";
			
			while(share>shares[i])
			cin >> share;
			
			}
		
			shares[i]=shares[i]-share;
		
			accountbalance[0]=accountbalance[0]+shares[i];
			
			break;
			}
		    }
		
		}
		
		//ADDING MONEY TO ACCOUT BALANCE
		
		 if(choice == 'M')
		 
		 {
		
		cout << "Enter the amount you want to add in your bank account :";
		
		cin >> amount;
		
		if(amount<0)
		
		{
		
		cout << " Enter valid amount : ";
		
		while(amount<0)
		
		cin >> amount;
		
		}
		
		accountbalance[0]=accountbalance[0]+amount;
		
		}
		
		// Withdrawing Money From account
		
		if(choice == 'W')
		 
		 {
		
		cout << "Enter the amount you want to withdraw from your bank account :";
		
		cin >> amount;
		
		if(amount>accountbalance[0])
		
		{
		
		cout << "Your withdrawing amount is grater than your account balance :\n Enter valid amount : ";
		
		while(amount>accountbalance[0])
		
		cin >> amount;
		
		}
		
		accountbalance[0]=accountbalance[0]-amount;
		
		}
		
		
		 if(choice=='E')
		   {
		
		    break;
		
		    }
		  }
		}
	
	
	//*********************************Withdraw Market Choices*********************************//
	
	
	
	
	if(ch=='A')
	{
	
	cout << "Enter the symbol of the company of which you want to buy the stock : ";
	
	cin >> search;
	
	for(int i=0; i<=rows; i++)
	
	{
	
		if(symbol[i]==search)
		{
	
		cout << "Enter how many shares you want to buy : ";
	
		cin >> shares[i];
	
		if(shares[i]>accountbalance[0])
		{
	
		cout << "Your account balance is not enough enter shares according to your account balance : ";
	
		cin >> shares[i]; 
	
		}
	
		accountbalance[0]=accountbalance[0]-shares[i];
		
		}
	     }
	
	}
	
	
	 if(ch =='R')
	
	{
	
	cout << "Enter the symbol of the company of which you want to sale the stock : ";
	
	cin >> search;

	for(int i=0; i<=rows; i++)
	
	{
	
		if(symbol[i]==search)
		{
	
		cout << "Enter how many shares you want to sale : ";
		
		cin >> share;
	
		if(share>shares[i])
		{
	
		cout << "You dont have much shares to sell Enter valid share : ";
		
		while(share>shares[i])
		cin >> share;
		
		}
	
		shares[i]=shares[i]-share;
	
		accountbalance[0]=accountbalance[0]+shares[i];
		
		}
	}
	
	}
	
	
	
	 if(ch == 'M')
	 
	 {
	
	cout << "Enter the amount you want to add in your bank account :";
	
	cin >> amount;
	
	accountbalance[0]=accountbalance[0]+amount;
	
	}
	
	 if(ch=='E')
	 {
	
	break;
	
	}

	}
		
	


	return 0;
}


//***********************************************************FUNCTIONS************************************************************


// This function reads the data from the text file and stores it in the 2D array
void readData(string stocks[][3], int rows, float CP[38])

{

        float f;

	ifstream fin;

	string str;

	fin.open("companies.txt");

	// Check if the file is open

	if (fin.is_open())

	{

		for (int i = 0; i < rows ; i++)

		{

			for(int j=0; j<3; j++)

     			   {

     			    if(j<2)

    				     {


    				      getline(fin,str,',');

   				       stocks[i][j]=str;

    				      }

    				      else if(j==2)

    				      {
				      
				      	
    				      fin >> f;

    				      CP[i]=f;

    				      }
          
			   }
		}
	}

	else

	{
		// Display an error message

		cout << "Error reading file!" << endl;

	}

	// Close the text file

	fin.close();

}



// This function updates the data stored in the 2D array

void updateData(float CP[38],float checkperci[38], float checkpercd[38], int rows)

{

	float d;

	int perc;

 	for(int i=0; i<rows; i++)

	   {

	 	  perc=(CP[i]*15/100)+1;
	 	  
	  	  d=(rand()%perc)+((rand()%100)/100.0);
	  	  
	  	  if(rand()%2==0 && (CP[i] + d) < checkperci[i] )

		  CP[i]=CP[i]+d;

	 	  else  if(rand()%2==1 && (CP[i]-d) > checkpercd[i] )

		  CP[i]=CP[i]-d;

    }

}



// This function shows the stock market screen

void showMarketScreen(string stocks[][3],float CP[],float PP[],float High[],float Low[], int rows, string topadvancer, string topdecliner, int totalshares)

{



         // Print the stock market screen

	cout<<setw(135)<<setfill('*')<<"\n"<<setfill(' ');

  	cout << "\033["<<44<<"m";

  	cout<<setw(70)<<right<<"Karachi Stock Market (Live)"<<setw(65)<<setfill(' ')<<"\033[0m"<<"\n";

  	cout << "\033["<<40<<"m";

 	cout << "\033["<<33<<"m";

  	cout << "Show Updates: Enter      Show Portfolio: P        Add Stock: A        Remove Stock: R         Add money to account: M         Exit: E"<<"\033[0m"<<"\n";
 
	cout << "\033["<<43<<"m";

        cout <<setw(10)<<left<<"Symbol"<<setw(50)<<left<<"Company Name"<<setw(20)<<left<<"Previous Price" << setw(20)<<left<<"Current Price"<<setw(10)<<right<<" High"<<setw(20)<<right<<" Low";

 	cout <<"\033[0m";

        cout<<endl;

        cout<<setw(135)<<setfill('*')<<"\n\n"<<setfill(' ');

        for(int i=0; i<rows ; i++)

	    {

	   	cout << setw(10)<< left << stocks[i][0];
	   	
		cout << setw(50)<< left << stocks[i][1];
	       
		cout << setw(20) << left<< PP[i];
	    
		if(CP[i]>PP[i])
	    
		{
	    
		cout << "\033["<<32<<"m"; 
	    
		cout << setw(10) << right<< CP[i]<<"\u2191";
	    
		cout <<"\033[0m";
	    
		}
	    
		else
	    
		{
	    
		cout << "\033["<<31<<"m"; 
	    
		cout << setw(10) << right<< CP[i]<<"\u2193";
	    
		cout <<"\033[0m";
	    
		}
	    
		cout<<setw(20)<<right<<High[i];
	    
		cout<<setw(20)<<right<<Low[i]<<endl;
	    
    	 }

     cout << endl << endl << endl;
     cout << "      :- TOP Advancer Symbol  "<< topadvancer<<endl<<endl;
     
     cout << "      :- TOP Decliner Symbol  "<< topdecliner<<endl<<endl;
     
     cout << "Total Shares Traded Today : "<<totalshares<<endl<<endl;

}


//***********************************************************************************************************************************************************//

// Show Portfolio
void showPortfolioScreen(string stocks[][3],float CP[],float PP[],float High[],float Low[],int gain_loss[],float shares[], int rows,int accountbalance[],string name)
{
	float T_gainloss=0;
	
	static int previousbalance=accountbalance[0];
	
	int newbalance=0;
	
	for(int i=0; i<rows; i++)
	
	{
	
		T_gainloss=T_gainloss+ gain_loss[i];
	
	}

	system("clear");
	
	cout<<setw(170)<<setfill('*')<<"\n"<<setfill(' ');

  	cout << "\033["<<44<<"m";

  	cout<<setw(80)<<right<<"Portfolio Owner : "<<name<< " (Live)"<<setw(80)<<setfill(' ')<<"\033[0m"<<"\n";

  	cout << "\033["<<40<<"m";

 	cout << "\033["<<33<<"m";

  	cout << "Show Updates: Enter         Live Market: L            Add Stock: A          Remove Stock: R             Add money to account: M       Withdraw Money:  W         Exit: E"<<"\033[0m"<<"\n";

	cout << "\033["<<43<<"m";

        cout <<setw(10)<<left<<"Symbol"<<setw(50)<<left<<"Company Name"<<setw(20)<<left<<"Previous Price" << setw(20)<<left<<"Current Price"<<setw(10)<<right<<"High"<<setw(20)<<right<<"Low"<<setw(20)<<right<<"Shares"<<setw(20)<<right<<"Gain/Loss";

 	cout <<"\033[0m";

        cout<<endl;

        cout<<setw(170)<<setfill('*')<<"\n\n"<<setfill(' ');

        for(int i=0; i<rows ; i++)

	     	{

	   	cout << setw(10)<< left << stocks[i][0];
	   	
		cout << setw(50)<< left << stocks[i][1];
	       
		cout << setw(20) << left<< PP[i];
	    
		if(CP[i]>PP[i])
	    
		{
	    
		cout << setw(10) << right<< CP[i]<<"\u2191";

		}
	    
		else
	    
		{
	   
	    
		cout << setw(10) << right<< CP[i]<<"\u2193";
	   
	    
		}
	    
		cout<<setw(20)<<right<<High[i];
	    
		cout<<setw(20)<<right<<Low[i];
		
		cout<<setw(20)<<right<<shares[i];
		
		 if(gain_loss[i]>0)
		
		{
		
		cout << "\033["<<32<<"m"; 
		  
		cout<<setw(20)<<right<<gain_loss[i]<<endl;
		
		cout <<"\033[0m";
		
		}
		
		else
	    
		{
	    
		cout << "\033["<<31<<"m"; 
	    
		cout<<setw(20)<<right<<gain_loss[i]<<endl;
	    
		cout <<"\033[0m";
	    
		}  
		
		}
        
        if(T_gainloss>0)
        
        {
        
        cout << "\n\nTotal Gain or Loss : ";
        
        cout << "\033["<<32<<"m"; 
          
        cout <<T_gainloss<<endl;
        
        cout <<"\033[0m";
       
        newbalance=previousbalance+T_gainloss;
        
        cout <<endl << "Previous Account Balance : " << "\033["<<32<<"m"<<accountbalance[0]<<endl<<endl;
        
        cout <<"\033[0m";
        
        cout << "New accout Balance : "<<"\033["<<32<<"m"<<newbalance<<endl<<endl;
        
        cout <<"\033[0m";
        
        previousbalance=newbalance;
        
        accountbalance[0]=newbalance;
        
        }
        
        else
    
        { 
    	cout << "\n\nTotal Gain or Loss : ";
        
        cout << "\033["<<31<<"m"; 
    
	cout <<T_gainloss<<endl;
    
        cout <<"\033[0m";
    
        newbalance=previousbalance+T_gainloss;
   
        cout <<endl << "Previous Account Balance : " << "\033["<<31<<"m"  << accountbalance[0] <<endl<<endl;
        
        cout <<"\033[0m";
        
        cout << "New accout Balance : "<< "\033["<<31<<"m"<< newbalance<<endl<<endl;
        
        previousbalance=newbalance;
        
        cout <<"\033[0m";
        
        accountbalance[0]=newbalance;
        
        }
        
        
        
        
        //************************************************************writing on file**********************************************************************//
        ofstream fout;
        
        fout.open("Portfolio.txt");
        
        
        fout<<setw(170)<<setfill('*')<<"\n"<<setfill(' ');

  	fout<<setw(80)<<right<<"Portfolio Owner : "<<name<< " (Live)"<<setw(80)<<setfill(' ')<< endl << endl;

  	fout << "Show Updates: Enter         Show Portfolio: P            Add Stock: A          Remove Stock: R             Add money to account: M       Withdraw Money:  W         Exit: E"<<endl<<endl;

        fout <<setw(10)<<left<<"Symbol"<<setw(50)<<left<<"Company Name"<<setw(20)<<left<<"Previous Price" << setw(20)<<left<<"Current Price"<<setw(10)<<right<<"High"<<setw(20)<<right<<"Low"<<setw(20)<<right<<"Shares"<<setw(20)<<right<<"Gain/Loss";

        fout<<endl<<endl;

        fout<<setw(170)<<setfill('*')<<"\n\n"<<setfill(' ');

        for(int i=0; i<rows ; i++)

       	  {

	   	fout << setw(10)<< left << stocks[i][0];
	   	
		fout << setw(50)<< left << stocks[i][1];
	       
		fout << setw(20) << left<< PP[i];
	    
		fout << setw(10) << right<< CP[i];
		
		fout<<setw(20)<<right<<High[i];
	    
		fout<<setw(20)<<right<<Low[i];
		
		fout<<setw(20)<<right<<shares[i];
		  
		fout<<setw(20)<<right<<gain_loss[i]<<endl;
          }
          
        fout << endl << endl << setw(50)<<setfill('*')<<"*";
          
        fout << "\n\nTotal Gain or Loss                : ";
          
        fout <<T_gainloss<<endl;
        
        fout <<endl << "Previous Account Balance          : " <<accountbalance[0]<<endl<<endl;
        
        fout << "New accout Balance                : "<<newbalance<<endl<<endl;

        fout <<setw(50)<<setfill('*')<<"*";
         
    	fout <<setw(50)<<setfill(' ')<<" ";
    	
    	
    	
}


