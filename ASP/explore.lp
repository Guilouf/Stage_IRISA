 %* mettre un espace avant pour pycharm...
Explore Metacyc database

cd C:\Documents and Settings\jnicolas\Mes documents\potsdam\ASP\metagenome

Call:
..\bin\clingo4.5.4 metacyc_18.5.lp hidden.lp explore.lp -c maxpath=2  --out-atomf="%s." --verbose=1 --stats=2 -n 0

*%



#const maxpath=1.

target(X):- is_a(X,"Menaquinols").
pw(Pathway):- produced(0,X); product(Reaction, X, _); 
	in_pathway(Reaction,Pathway). 
pw(Pathway2):- pw(Pathway1); is_a(Pathway1,SuperPathway); is_a(Pathway2,SuperPathway); Pathway1!= Pathway2.

1{t(X):target(X)}1.

path(I+1, EC, Reaction, R, CNR):- 
	produced(I,P); I<maxpath; product(Reaction, P, _); ec_number(Reaction,EC);
	reactant(Reaction, R, _); common_name(R, CNR); pw(Pathway); in_pathway(Reaction,Pathway);
	not hidden(R); not produced(J,R):J=0..I-1.

produced(0,X):-t(X).
produced(I,P):- path(I,_,_,P,_).

%pathway(I,Pathway):- path(I,_,Reaction,_,_); in_pathway(Reaction,Pathway); I=0..maxpath.

%class(C):- produced(_,P); is_a(P,C).


mreac(Reac):- ec_number(Reac, e(A,B)).

	
#show.
#show mreac/1.
#show vitamin(V): t(X); common_name(X, V).
#show path/5.
#show pathway(PW): pw(X); common_name(X, PW).
%#show class/1.
