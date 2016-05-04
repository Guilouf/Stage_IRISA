
 %* ###############################################
Utilitaires
################################################ *%
#const maxstrain = 10. %'max de souches recherchées'

% Une vitamine pour laquelle il y a des Ec présents ds aucune souches
impossibleV(V) :- not enzymeV(V,Ec) : total_match(V,S,T,Ec) ; vitamin(V).


 %* ###############################################
 1 strain having all enzyme of a vitamin pathway OK
################################################ *%
% total vrai si vrai pour tout enzymeV
completeStrainV(S,V) :- total_match(V,S,T,Ec) : enzymeV(V,Ec) ; vitamin(V) ; strain(S) ; enzymeV(V,_).

 %* ################################################################
 2 minimal set of COMPLETE strains having enzymes of all vitamins
 Quel ensemble de souches peut faire toutes les vitamines ?
################################################################## *%
1{minCompletS(S) : strain(S)} maxstrain .    %'definition du choix: min est max n souches parmi d autres..

:- minCompletS(S) ; not completeStrainV(S,_).  %'ca filtre le choix, n est pas complet si n est pas completstrainV

coveredVitamin(V) :- minCompletS(S) ; completeStrainV(S,V). %'une vit est couverte si elle est completeStrainV
%:- not coveredVitamin(V) ; not impossibleV(V) ; vitamin(V). %'il n existe pas de vit v non couverte, qui n est pas une vit imposs

#minimize {1@1,S:minCompletS(S)}.
#maximize {1@1,V:coveredVitamin(V)}.


 %* #######################################################
 3 minimal set of strains having enzymes of all vitamins
 Quel ensemble de souche peuvent se completer pour faire une vitamine
 ####################################################### *%
% 1{minStrain(S): strain(S)} maxstrain.  %' choix de souches
 1{minStrain(S,V): strain(S), vitamin(V)} maxstrain.  %' choix de souches

coveredEnzyme(V,Ec) :- total_match(V,S,_,Ec) ;  minStrain(S,V) . %'enzymeV couverte si présente ds une souche de l ensmbl

% heu le commenter enlève des enzymes: vit1 1..10, celle de la souche1... (vit3 com, sinon insat..)
% pk qd c com, les vit1 1..10 se retrouvent en uncovered alr qu'ils sont en total match?? a cause de min strain?
% ouais c'est a cause de la minimisation, du coup il me sort que ceux de la souche 2..

:- not coveredEnzyme(V,Ec) ; not impossibleV(V) ; enzymeV(V,Ec) . %'il nexiste pas denzyme non couverte?(ni de vit du coup?) qui ne soit pas en impossibleV

uncovered(V,Ec) :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) . %'une enz de pathway pas présente ds les bactéries


#minimize {1@1,S:minStrain(S,V)}.
%#maximize {1@1,V,Ec:coveredEnzyme(V,Ec)}.


% essai lucas
%2 { choosen(S): souche(S)} maxstrain.
%1 { target(V): vitamin(V) } 1.
%choosen_enzymes(E) :- choosen(S) ; produce(S,E). %'ensembl des enzymes d un ensembl de souches
%:- target(V) ; need(V,E) ; not choosen_enzymes(E). %'elimine le enz qui ne completent pas



%todo Partie show:

 %* Utilitaires *%
%#show impossibleV/1.

 %* 1 Question OK *%
%#show completeStrainV/2.

 %* 2 Question *%
#show coveredVitamin/1.
#show minCompletS/1.

 %* 3 Question *%
%#show coveredEnzyme/2.
%#show uncovered/2.
%#show minStrain/2.


%#show enzymeV/2.
%#show total_match/4.


%* Tableau croisé: pr une vitamine *%
%#show enzymeV/2.
%#show full_match/4.
%#show rest_match/4.