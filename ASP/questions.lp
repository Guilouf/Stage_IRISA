
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



#const vitamin = b12.  %'permet en plus d'é"viter les doublons"

1{minStrainVitamin(S,vitamin) : strain(S), not completeStrainV(S,vitamin)} maxstrain .    %'definition du choix: min est max n souches parmi d autres.., pas de complete strain


coveredEnzymeVitamin(S,vitamin,Ec) :- total_match(vitamin,S,_,Ec) ;  minStrainVitamin(S,vitamin) . %' enzymeV présente ds une souche choisie pour cette vitamine

coveredEnzymeVitamin(vitamin,Ec) :- coveredEnzymeVitamin(S,vitamin,Ec).

:- not coveredEnzymeVitamin(vitamin,Ec) ; not impossibleV(vitamin) ; enzymeV(vitamin,Ec) . %'il nexiste pas denzyme non couverte qui ne soit pas en impossibleV


vitaminTaxon_one(vitamin,(T,U)) :- minStrainVitamin(S,vitamin) ; taxonomy(S,T,U).

enzymeSuccStrain(V,Ec1,Ec2,S) :- enzymeSucc(V,Ec1,Ec2) ; minStrainVitamin(S,vitamin,Ec1) ; minStrainVitamin(S,vitamin,Ec2). %'ec successif pour la mm souche


#minimize {1@4,S:minStrainVitamin(S,vitamin)}.
#minimize {1@3,T:vitaminTaxon_one(vitamin,T)}.
#maximize {1@2,S,Ec1,Ec2:enzymeSuccStrain(vitamin,Ec1,Ec2,S) }.
#maximize {1@1,S,Ec:coveredEnzymeVitamin(S,vitamin,Ec)}. %'maximiser la superposition des voies'





%todo Partie show:

 %* Utilitaires *%
%#show impossibleV/1.


 %* 1 Question OK *%
%#show completeStrainV/2.

 %* 2 Question *%
%#show enzymeV/2.
#show minStrainVitamin/2.
%#show twoStrainsVitamin/2.
%#show enzymeSuccStrain/4.
%#show oneStrainVitamin/3.
%#show vitaminTaxon_one(T): vitaminTaxon_one(vitamin, (T,U)) .



%#show minSV(S,V) : minStrain(S,V,_).

%#show enzymeV/2.
%#show total_match/4.


%* Tableau croisé: pr une vitamine *%
%#show enzymeV/2.
%#show full_match/4.
%#show rest_match/4.