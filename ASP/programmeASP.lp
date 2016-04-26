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

%définition du pathway, des vitamines et souches
pathwayV(V,P) :- superpathwayV(V,SPN) ; common_name(SP,SPN) ; is_a(P,SP).
vitamin(V) :- superpathwayV(V,_).
strain(S) :- num_access(S,_,_).

superpathwayV(k2_7,"superpathway of menaquinol-7 biosynthesis").
superpathwayV(b9,"superpathway of tetrahydrofolate biosynthesis").
superpathwayV(b12,"adenosylcobalamin biosynthesis I (early cobalt insertion)").

%les enzymes appartenants aux vitamines
enzymeV(V,Ec) :-    in_pathway(R,P) ;
                    ec_number(R,Ec) ;
                    pathwayV(V,P).

%les enzymes appartenants aux souches, et correspondant aux enzymes du pathway
enzymeS(V,S,EcS,T) :- enzymeV(V,EcV);
                     uniprot(EcS,Uniref);
                     num_access(S,Uniref,_); %888 changer ici pour refseq
                     map(EcV,EcS,T).

%comptage des occurences de enzymesV
statV(V,T,N) :- vitamin(V) ; T=(3..4) ; N=#count {enzymeV(V,Ec): enzymeV(V,Ec),size_ec(Ec,T)}.

%Pareil que enzyme S mais avec plus d'args. Pour faire full_match, EcV = EcS..
matched(V,S,T,EcV,EcS) :-
                        enzymeV(V,EcV) ;
                        uniprot(EcS,Uniref);
                        num_access(S,Uniref,"PRIMAIRE"); %888 changer ici pour refseq
                        map(EcV,EcS,T).

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

%le système de matchs
full_match(V,S,T,Ec) :- matched(V,S,T,Ec,Ec); Ec!=ec(3,6,1,o).   % , S="FN806773".
rest_match(V,S,T,EcS) :- match_rest(V,S,T,EcS,EcC) ; EcS!=ec(3,6,1,o).   % , S="FN806773".
total_match(V,S,T,EcS) :- full_match(V,S,T,EcS).
total_match(V,S,T,EcS) :- rest_match(V,S,T,EcS).


% todo Partie 3 questions

#const maxstrain = 5.

 %* 1 strain having all enzyme of a vitamin pathway *%
% total vrai si vrai pour tout enzymeV
completeStrainV(S,V) :- total_match(V,S,T,Ec) : enzymeV(V,Ec) ; vitamin(V) ; strain(S) .


 %* 2 minimal set of strains having enzymes of all vitamins *%
%1{minCompletS(S) : strain(S)} maxstrain .    %88 definition du choix: min est max 5souches parmi d'autres..
%
%:- minCompletS(S) ; not completeStrainV(S,_).  %88 ca filtre le choix, n est pas complet si n est pas completstrainV
%
%coveredVitamin(V) :- minCompletS(S) ; completeStrainV(S,V). %88 une vit est couverte si elle est completeStrainV
%:- not coveredVitamin(V) ; vitamin(V). %88
%
%#minimize {minCompletS(S): strain(S)}.

%score(N) :- N={minCompletS(_)}.
%#minimize {N@1,N: score(N)}.  %88 S unsafe..

 %* 3 minimal set of strains having enzymes of all vitamins *% %'eh cest la mm prob..
% 1{minStrain(S): strain(S)}maxstrain.  %88' choix

% coveredEnzyme(V,Ec) :- enzymeStrainVitamin(S,V,Ec) ; minStrain(S) . %88
% :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) . %88'il nexiste pas denzyme non couverte?
% #minimize {minStrain(S): minStrain(S), strain(S)}.



 %* Mon essai des 3 questions*%
%2eme Q souches qui ont des enzymes dans ttes les vits
strainAllPartV(S) :- total_match(V,S,T,Ec) : vitamin(V) ; strain(S).

%3eme

 %* PARTIE SHOW*%
#show.

 %*Mes questions  *%
#show strainAllPartV/1.  %'marche, mm si chez moi peut pas verif

 %*Les 3 télés  *%
#show completeStrainV/2.



 %* Tableau croisé: pr une vitamine *%
#show enzymeV/2.
#show full_match/4.
#show rest_match/4.
#show total_match/4.
