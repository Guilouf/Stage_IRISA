
 %* ###############################################
Utilitaires
################################################ *%
#const maxstrain = 2. %'max de souches recherchées ok alors maintenant qd on en met - de 10 ca foire..
%ok le maxstrain à l'air pour la totalité des vits
%qd on met 10 on a un ensemble de 5 souches


% Une vitamine pour laquelle il y a des Ec présents ds aucune souches
impossibleV(V) :- not enzymeV(V,Ec) : total_match(V,S,T,Ec) ; vitamin(V).


 %* ###############################################
 1 strain having all enzyme of a vitamin pathway OK
################################################ *%
% total vrai si vrai pour tout enzymeV
completeStrainV(S,V) :- total_match(V,S,T,Ec) : enzymeV(V,Ec) ; vitamin(V) ; strain(S) ; enzymeV(V,_).

 %* ################################################################
 2 minimal set of COMPLETE strains having enzymes of all vitamins
 Quel ensemble de souches peut faire toutes les vitamines ? non c'est pas ca..
 Quel ensemble de souches completes peut faire la totalité des vitamines ?
=> quelles ensemble de souches peut produire UNE vitamine ?
    - la question 3 repond à cette question du coup
################################################################## *%


 %*
1{minCompletS(S) : strain(S)} maxstrain .    %'definition du choix: min est max n souches parmi d autres..

:- minCompletS(S) ; not completeStrainV(S,_).  %'ca filtre le choix, n est pas complet si n est pas completstrainV

coveredVitamin(V) :- minCompletS(S) ; completeStrainV(S,V). %'une vit est couverte si elle est completeStrainV
%:- not coveredVitamin(V) ; not impossibleV(V) ; vitamin(V). %'il n existe pas de vit v non couverte, qui n est pas une vit imposs

#minimize {1@1,S:minCompletS(S)}.
#maximize {1@1,V:coveredVitamin(V)}.

*%

 %* #######################################################
 3 minimal set of strains having enzymes of all vitamins
 Quel ensemble de souche peuvent se completer pour faire une vitamine
 ####################################################### *%
 1{minStrain(S): strain(S)} maxstrain.  %' choix de souches
 1{minStrain(S,V,Ec): minStrain(S), vitamin(V), enzymeV(V,Ec)}.  %' choix de souches


coveredEnzyme(V,Ec) :- total_match(V,S,_,Ec) ;  minStrain(S,V,Ec) . %'enzymeV couverte si présente ds une souche de l ensmbl


:- not coveredEnzyme(V,Ec) ; not impossibleV(V) ; enzymeV(V,Ec) . %'il nexiste pas denzyme non couverte?(ni de vit du coup?) qui ne soit pas en impossibleV


uncovered(V,Ec) :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) . %'une enz de pathway pas présente ds les bactéries


minStrain(S,V) :- minStrain(S,V,Ec).

twoStrains(V) :- minStrain(S1,V) ; minStrain(S2,V) ; taxonomy(S1,T,U) ; not taxonomy(S2,T,U).

vitaminTaxon(V,(T,U)) :- minStrain(S,V) ; taxonomy(S,T,U).

#minimize {1@3,S:minStrain(S)}.
#minimize {1@2,S,V:minStrain(S,V,Ec)}.
#maximize {1@1,S,V,Ec:minStrain(S,V,Ec)}. %'maximiser la superposition des voies'
#minimize {1@0,V,T:vitaminTaxon(V,T)}.
%#maximize {1@1,V,Ec:coveredEnzyme(V,Ec)}.

%todo exclusions
%:- minCompletS("NC_017486.1").
%:- minCompletS("CDAG00000000.1").
%:- minCompletS("NC_017486.1") ; minCompletS("CDAG00000000.1").
%:- minStrain("CDAG00000000.1",_).
%:- minStrain("NC_017486.1",_).
%:- minStrain("CDAG00000000.1",_) ; minStrain("NC_017486.1",_).

%todo Partie show:

 %* Utilitaires *%
%#show impossibleV/1.


 %* 1 Question OK *%
%#show completeStrainV/2.

 %* 2 Question *%
%#show coveredVitamin/1.
%#show vitnon_couv(V): not coveredVitamin(V), vitamin(V). %'b12 pas couverte, besoin de collaboration'
%#show minCompletS/1.

 %* 3 Question *%
%#show coveredEnzyme/2.
%#show uncovered/2.
%#show minStrain/1.
%#show minStrain/3.
%#show minStrain/2.
%#show vitaminTaxon/2.
%#show twoStrains/1.

%#show minSV(S,V) : minStrain(S,V,_).

%#show enzymeV/2.
%#show total_match/4.


%* Tableau croisé: pr une vitamine *%
%#show enzymeV/2.
%#show full_match/4.
%#show rest_match/4.