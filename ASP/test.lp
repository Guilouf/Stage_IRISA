 %*
common_name(reaction_id or enzyme_id or pathway_id or compound_id , common_name).
direction(reaction_id, reaction_direction).
ec_number(reaction_id, ec(x,x,x,x) ou ec(x,x,x)).
reactant(reaction_id, reactant_id, stochio)
product(reaction_id, product_id, stochio).
in_pathway(reaction_id, pathway_id).
catalysed_by(reaction_id, enzyme_id).
uniprotID(enzyme_id, uniprot_id).
is_a(class or compound, class_id).
is_a(pathway_id, pathway_id).

#Memmo ma base#
uniprot( ec(2,1,1,72),"A0A0L7Y7H5").
num_access("NC_020229.1","A0A0L7Y7H5").

*%


 %*
% selectionne un truc qui est un menaquinol
%target(X) :- is_a(X,"Menaquinols").

% selec la reaction qui produit le truc
%la_reac(Reac) :- product(Reac, X, Stoc).

% selec le numero ec de la reaction
%numero_ec(Ec) :- ec_number(Reac, Ec).

*%


%a partir de ca on peut retrouver des reactions associés un pathway chez mes bactéries
%il manque pr tetrahydro 1 ec(3.6.1.67).. et RXN-9311", ec(3,1,2,28)=> pas chez mes trucs c tt..
 %*
react_path(Hier_inf, Reaction_id,  Ec) :-
        in_pathway(Reaction_id, Hier_inf) ;

        niveau(I, Hier_inf);

        %uniprot(Ec, Uniref);
        %num_access(Refseq, Uniref);
        ec_number(Reaction_id, Ec).
*%

%le recursif pour retrouver les is_a inferieurs
%"superpathway of menaquinol-7 biosynthesis"
%"superpathway of tetrahydrofolate biosynthesis"
%"adenosylcobalamin biosynthesis I (early cobalt insertion)"

%N = #count {react_path(Hier_inf, Reaction_id,  Ec): react_path(Hier_inf, Reaction_id,  Ec)}

%compt(Hier_inf, N) :- react_path(Hier_inf, Reaction_id,  Ec).

 %*
niveau(0, Hier_inf) :- is_a(Hier_inf, Pathway_id); common_name(Pathway_id, "superpathway of tetrahydrofolate biosynthesis").
niveau(I, Hier_inf) :- is_a(Hier_inf, Hier_sup) ; niveau(I-1,Hier_sup).
*%
%ec_trois(X) :- uniprot( ec(_,_,_,_), X).

%donc pas d'acc uniprot en commun..
%uni_comun(Uniref) :- uniprot( _, Uniref) ; uniprotID(_, Uniref).

#show.

%c presque bon mais il me manque 2 ec au niveau du gtp..
#show react_path/3.

#show ec_trois/1.
#show compt/2.


%cool ca marche, c'est pour montrer le nom des paths
%#show nom_path(Nom): react_path(Autrepath, Reaction_id, Uniref, Ec) ; common_name(Autrepath, Nom).

%#show uni_comun/1.
 %*
%bon yen a 5
niveau(0,Hier_inf) :- is_a(Hier_inf, "FOLSYN-PWY").
niveau(I,Hier_inf) :- is_a(Hier_inf, Hier_sup) ; niveau(I-1,Hier_sup).
*%

%#show niveau/2.

%Partie Jaques


%définition du pathway, des vitamines et souches
pathwayV(V,P) :- superpathwayV(V,SPN) ; common_name(SP,SPN) ; is_a(P,SP).
vitamin(V) :- superpathwayV(V,_).
strain(S) :- num_access(S,_,_).
superpathwayV(k2_7,"superpathway of menaquinol-7 biosynthesis").
superpathwayV(b9,"superpathway of tetrahydrofolate biosynthesis").
%superpathwayV(b12,"adenosylcobalamin biosynthesis I (early cobalt insertion)").

%les enzymes appartenants aux vitamines
enzymeV(V,Ec) :-    in_pathway(R,P) ;
                    ec_number(R,Ec) ;
                    pathwayV(V,P).

%les enzymes appartenants aux souches, et correspondant aux enzymes du pathway
enzymeS(V,S,EcS,T) :- enzymeV(V,EcV);
                     uniprot(EcS,Uniref);
                     num_access(S,Uniref,_); %888 changer ici pour refseq
                     map(EcV,EcS,T).

%comptage des occurences de enzymesS
%N=#count {enzymeS(V,S,Ec,T): enzymeS(V,S,Ec,T)}. equivalent: %N={enzymeS(_,_,_,_)}. %ce qui a a la place des _ n'est definit qu'entre les {}

%statS(V,S,T,N) :- vitamin(V) ; strain(S) ; type(T) ; N={enzymeS(V,S,_,T)}.

%statS(V,S,T,N) :- vitamin(V) ; strain(S) ; type(T) ; N={enzymeS(_,_,_,_)}.

%comptage des occurences de enzymesV
statV(V,T,N) :- vitamin(V) ; T=(3..4) ; N=#count {enzymeV(V,Ec): enzymeV(V,Ec),size_ec(Ec,T)}.

%Pareil que enzyme S mais avec plus d'args. Pour faire full_match, EcV = EcS..
matched(V,S,T,EcV,EcS) :-
                        enzymeV(V,EcV) ;
                        uniprot(EcS,Uniref);
                        num_access(S,Uniref,"PRIMAIRE"); %888 changer ici pour refseq
                        map(EcV,EcS,T).



%visiblement le not marche pas comme je voudrais...=>ca marche par ensemble de variables...
%%%%%%%%%%%%%%%%%%%%%%%% FAUDRA faire gaffe quand on voudra regarder plusieurs souches etc.=> pas l'air de poser pb
match_rest(V,S,T,EcV,EcSS) :- matched(V,S,T,EcV,EcSS) ; not matched(V,S,_,EcV,EcV) .

%mappeur d'EC
map(ec(X,Y,Z,T),ec(X,Y,Z,T),t(4,4)) :- enzymeV(V,ec(X,Y,Z,T)).
map(ec(X,Y,Z,T),ec(X,Y,Z),t(4,3)) :- enzymeV(V,ec(X,Y,Z,T)).

map(ec(X,Y,Z),ec(X,Y,Z,T),t(3,4)) :- enzymeV(V,ec(X,Y,Z)) ; uniprot(ec(X,Y,Z,T),_).
map(ec(X,Y,Z),ec(X,Y,Z),t(3,3)) :- enzymeV(V,ec(X,Y,Z)).

%type de correspondance
type(t(4,4)). type(t(4,3)). type(t(3,4)). type(t(3,3)).

size_ec(ec(X,Y,Z,T),4) :- enzymeV(V,ec(X,Y,Z,T)).
size_ec(ec(X,Y,Z),3) :- enzymeV(V,ec(X,Y,Z)).



 %* PARTIE SHOW*%

 %*Les show enzyme:  *%
%#show enzymeV/2.
%#show enzymeV(V,Ec): enzymeV(V,Ec), Ec=ec(X,Y,Z,T).
%#show enzymeS(V,S,EcS,T): enzymeS(V,S,EcS,T) , S="FN806773". %888 combine les match 3 et 4..je devrais partir de là pr le match
%#show enzymeS/4.


 %*Les show stats:  *%
%#show statS(V,S,N): statS(V,S,(3,4),N).
%#show statS/4.
%#show statV/3.


%n'imprime pas ceux qui sont à 0 occurences
%#show statS(V,S,T,N): statS(V,S,T,N), not statS(V,S,T,(0)).

%pour tab ecv4, ou ecV3 si on change le premire
%#show statS(V,S,T,N):  statS(V,S,T,N) , T=t(4,3..4).

 %*AOn reprend depuis le début... pour B9 et CIRM => mauvais exemple..*%
%#show enzymeV/2. %montre les ec du pathway: 10
%#show matched(V,S,T,EcV,EcS) : matched(V,S,T,EcV,EcS) , S="FN806773".
%#show match_final(V,S,T,EcS,EcSS) : match_rest(V,S,T,EcS,EcSS).% , S="FN806773".
%#show full_match(V,S,Ec) : full_match(V,S,_,Ec) , S="FN806773". %888avec ca j'obtiens ce que jattend'
% ok il me reste a faire une fonction pour dire que 2 ec commencant par le mm prefixe sont le mm... en qq sorte

 %*AOn reprend depuis le début... pour K2 et CIRM *%
%#show enzymeV/2. %montre les ec du pathway: 10
%#show enzymeS(V,S,EcS,T): enzymeS(V,S,EcS,T) , S="FN806773".
%#show matched(V,S,T,EcV,EcS) : matched(V,S,T,EcV,EcS) , S="FN806773".  % c'est logique quil yen ai une de +1 2.5.1'
%#show match_final(V,S,T,EcS,EcSS) : match_rest(V,S,T,EcS,EcSS) , S="FN806773". % plus qua additioner full match, donne 2
%#show full_match(V,S,T,Ec,Ec) : matched(V,S,T,Ec,Ec) , S="FN806773". %888avec ca j'obtiens ce que jattend', donne 5

%Pour reunir les deux c une technique..
%#show match_final(V,S,T,EcS,EcSS) : match_rest(V,S,T,EcS,EcSS) , S="FN806773".
%#show match_final(V,S,T,Ec,Ec) : matched(V,S,T,Ec,Ec) , S="FN806773".




 %* Tableau croisé: pr une vitamine *%
#show enzymeV/2.  %enlever 3.6.1.o
#show full_match(V,S,T,Ec) : matched(V,S,T,Ec,Ec), Ec!=ec(3,6,1,o).% , S="FN806773".
#show rest_match(V,S,T,EcS) : match_rest(V,S,T,EcS,EcC) , EcS!=ec(3,6,1,o).% , S="FN806773".

 %* Vieux tableau nouveau.. *%

%statS(V,S,N) :- vitamin(V), strain(S), N={matched(V,S,T,Ec,Ec)}. %888 match complet
%statS(V,S,N) :- vitamin(V), strain(S), N={match_rest(V,S,T,EcS,EcC)}. %888 match restant

%statS(V,S,N,NM) :- vitamin(V), strain(S), N={matched(V,S,T,Ec,Ec)}, NM={match_rest(V,S,T,EcS,EcC)}. %88 fait les 2
%#show statS/3.