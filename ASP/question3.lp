 %* #######################################################
 3 minimal set of strains having enzymes of all vitamins
 Quel ensemble de souche peuvent se completer pour faire une vitamine
 ####################################################### *%



 1{minStrain(S): strain(S)} maxstrain.  %' choix de souches
 1{minStrain(S,V,Ec): minStrain(S), vitamin(V), enzymeV(V,Ec)} .  %' choix de souches


coveredEnzyme(V,Ec) :- total_match(V,S,_,Ec) ;  minStrain(S,V,Ec) . %'enzymeV couverte si présente ds une souche de l ensmbl


:- not coveredEnzyme(V,Ec) ; not impossibleV(V) ; enzymeV(V,Ec) . %'il nexiste pas denzyme non couverte?(ni de vit du coup?) qui ne soit pas en impossibleV


uncovered(V,Ec) :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) . %'une enz de pathway pas présente ds les bactéries


enzymeSuccStrain(V,Ec1,Ec2,S) :- enzymeSucc(V,Ec1,Ec2) ; minStrain(S,V,Ec1) ; minStrain(S,V,Ec2). %'ec successif pour la mm souche


minStrain(S,V) :- minStrain(S,V,Ec).

twoStrains(V) :- minStrain(S1,V) ; minStrain(S2,V) ; taxonomy(S1,T,U) ; not taxonomy(S2,T,U).

vitaminTaxon(V,(T,U)) :- minStrain(S,V) ; taxonomy(S,T,U).




#minimize {1@4,S:minStrain(S)}.
#minimize {1@3,V,T:vitaminTaxon(V,T)}.
#maximize {1@2,S,Ec1,Ec2:enzymeSuccStrain(V,Ec1,Ec2,S) }.
#maximize {1@1,S,V,Ec:minStrain(S,V,Ec)}. %'maximiser la superposition des voies'

%#maximize {1@1,V,Ec:coveredEnzyme(V,Ec)}.


% je sais plus ce que cela faisait..
%#minimize {1@4,S:minStrain(S)}.
%#minimize {1@3,S,V:minStrain(S,V,Ec)}.
%#maximize {1@2,S,V,Ec:minStrain(S,V,Ec)}. %'maximiser la superposition des voies'
%#minimize {1@1,V,T:vitaminTaxon(V,T)}.

 %* 3 Question *%
%#show coveredEnzyme/2.
%#show uncovered/2.
%#show minStrain/1.


#show minStrain/3.



% ca fait tout bugger ce show là, explose la memmoire attention
%#show minStrainWesh(S,VV,Ec) : minStrain(S,VV,Ec), VV=b12.



%#show enzymeV/2.
%#show full_match/4.
%#show rest_match/4.


%#show minStrain/2.
%#show vitaminTaxon/2.
%#show twoStrains/1.