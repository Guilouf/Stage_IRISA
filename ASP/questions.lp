
#const maxstrain = 10.

 %* ###############################################
 1 strain having all enzyme of a vitamin pathway
################################################ *%
% total vrai si vrai pour tout enzymeV
completeStrainV(S,V) :- total_match(V,S,T,Ec) : enzymeV(V,Ec) ; vitamin(V) ; strain(S) ; enzymeV(V,_).

 %* ################################################################
 2 minimal set of COMPLETE strains having enzymes of all vitamins
################################################################## *%
1{minCompletS(S) : strain(S)} maxstrain .    %'definition du choix: min est max n souches parmi d autres..

:- minCompletS(S) ; not completeStrainV(S,_).  %'ca filtre le choix, n est pas complet si n est pas completstrainV

coveredVitamin(V) :- minCompletS(S) ; completeStrainV(S,V). %'une vit est couverte si elle est completeStrainV
%:- not coveredVitamin(V) ; vitamin(V). %'il n existe pas de vit v non couverte, pas compris a quoi ca sert..

#minimize {1@1,S:minCompletS(S)}.
#maximize {1@1,V:coveredVitamin(V)}.



 %* #######################################################
 3 minimal set of strains having enzymes of all vitamins REFAIRE PAS CLAIR
 ####################################################### *%
 1{minStrain(S): strain(S)} maxstrain.  %' choix de souches

coveredEnzyme(V,Ec) :- total_match(V,S,_,Ec) ;  minStrain(S) . %'enzymeV couverte si présente ds une souche de l ensmbl

% heu le commenter enlève des enzymes: vit1 1..10, celle de la souche1... (vit3 com, sinon insat..)
% pk qd c com, les vit1 1..10 se retrouvent en uncovered alr qu'ils sont en total match?? a cause de min strain?
% ouais c'est a cause de la minimisation, du coup il me sort que ceux de la souche 2..

% :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) . %'il nexiste pas denzyme non couverte?(ni de vit du coup?)
% faut trouver un moyen de refaire ca..
uncovered(V,Ec) :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) . %'une enz de pathway pas présente ds les bactéries




#minimize {1@1,S:minStrain(S)}.
%#maximize {1@1,V,Ec:coveredEnzyme(V,Ec)}.

%todo Partie show:

 %* 1 Question OK *%
%#show completeStrainV/2.

 %* 2 Question *%
%#show coveredVitamin/1.

 %* 3 Question *%
#show coveredEnzyme/2.
#show uncovered/2.
%#show minStrain/1.



%#show coveredEnzyme/2.
%#show minStrain/1.
%#show uncovered/2.


%#show enzymeV/2.
%#show total_match/4.


%* Tableau croisé: pr une vitamine *%
%#show enzymeV/2.
%#show full_match/4.
%#show rest_match/4.