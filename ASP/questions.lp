
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
1{minStrainVitamin(S,V) : strain(S)} maxstrain :- vitamin(V).    %'definition du choix: min est max n souches parmi d autres..

1{minStrainVitamin(S,V,Ec): minStrainVitamin(S,V), enzymeV(V,Ec)}.  %' choix des enzymes

%!!!!! faire gaffe, ce sont les enzymeV dc pas forcément ceux qui sont dans la souche.. les modèles ont l'air bon
% on dirait que ca n'a pas fixé la vitamine..

coveredEnzymeVitamin(V,Ec) :- total_match(V,S,_,Ec) ;  minStrainVitamin(S,V,Ec) . %' enzymeV présente ds une souche choisie pour cette vitamine


:- not coveredEnzyme(V,Ec) ; not impossibleV(V) ; enzymeV(V,Ec) . %'il nexiste pas denzyme non couverte qui ne soit pas en impossibleV


minStrain(S,V) :- minStrain(S,V,Ec).

twoStrainsVitamin(V) :- minStrainVitamin(S1,V) ; minStrainVitamin(S2,V) ; taxonomy(S1,T,U) ; not taxonomy(S2,T,U).

vitaminTaxon_one(V,(T,U)) :- minStrainVitamin(S,V) ; taxonomy(S,T,U).

#minimize {1@3,S:minStrainVitamin(S,V)}.
#maximize {1@2,S,V,Ec:minStrainVitamin(S,V,Ec)}. %'maximiser la superposition des voies'
#minimize {1@1,V,T:vitaminTaxon_one(V,T)}.

*%

#const vitamin = b12.  %'permet en plus d'é"viter les doublons"

1{minStrainVitamin(S,vitamin) : strain(S), not completeStrainV(S,vitamin)} maxstrain .    %'definition du choix: min est max n souches parmi d autres..

1{minStrainVitamin(S,vitamin,Ec): minStrainVitamin(S,vitamin), enzymeV(vitamin,Ec)}.  %' choix des enzymes


coveredEnzymeVitamin(S,vitamin,Ec) :- total_match(vitamin,S,_,Ec) ;  minStrainVitamin(S,vitamin,Ec) . %' enzymeV présente ds une souche choisie pour cette vitamine

coveredEnzymeVitamin(vitamin,Ec) :- coveredEnzymeVitamin(S,vitamin,Ec).

:- not coveredEnzymeVitamin(vitamin,Ec) ; not impossibleV(vitamin) ; enzymeV(vitamin,Ec) . %'il nexiste pas denzyme non couverte qui ne soit pas en impossibleV

:- minStrainVitamin(S,vitamin,Ec) ; not coveredEnzymeVitamin(S,vitamin,Ec).

minStrainVitamin(S,vitamin) :- minStrainVitamin(S,vitamin,Ec).

twoStrainsVitamin(vitamin,Ec) :- minStrainVitamin(S1,vitamin,Ec) ; minStrainVitamin(S2,vitamin,Ec); S1!=S2. %; taxonomy(S1,T,U) ; not taxonomy(S2,T,U).

oneStrainVitamin(vitamin,S1,Ec) :- minStrainVitamin(S1,vitamin,Ec) ; not twoStrainsVitamin(vitamin,Ec). %'represente les ec fait par une seul souche


vitaminTaxon_one(vitamin,(T,U)) :- minStrainVitamin(S,vitamin) ; taxonomy(S,T,U).

enzymeSuccStrain(V,Ec1,Ec2,S) :- enzymeSucc(V,Ec1,Ec2) ; minStrainVitamin(S,vitamin,Ec1) ; minStrainVitamin(S,vitamin,Ec2).


#minimize {1@4,S:minStrainVitamin(S,vitamin)}.
#maximize {1@1,S,Ec:minStrainVitamin(S,vitamin,Ec)}. %'maximiser la superposition des voies'
#minimize {1@3,T:vitaminTaxon_one(vitamin,T)}.
#maximize {1@2,S,Ec1,Ec2:enzymeSuccStrain(vitamin,Ec1,Ec2,S) }.


 %* #######################################################
 3 minimal set of strains having enzymes of all vitamins
 Quel ensemble de souche peuvent se completer pour faire une vitamine
 ####################################################### *%


  %*
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

*%

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
%#show enzymeV/2.
%#show minStrainVitamin/3.
%#show twoStrainsVitamin/2.
%#show enzymeSuccStrain/4.
#show oneStrainVitamin/3.
%#show vitaminTaxon_one(T): vitaminTaxon_one(vitamin, (T,U)) .

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