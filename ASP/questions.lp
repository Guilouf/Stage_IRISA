#const maxstrain = 10.

 %* 1 strain having all enzyme of a vitamin pathway *%
% total vrai si vrai pour tout enzymeV
completeStrainV(S,V) :- total_match(V,S,T,Ec) : enzymeV(V,Ec) ; vitamin(V) ; strain(S) .


 %* 2 minimal set of COMPLETE strains having enzymes of all vitamins *%
1{minCompletS(S) : strain(S)} maxstrain .    %88 definition du choix: min est max 5souches parmi d'autres..

:- minCompletS(S) ; not completeStrainV(S,_).  %88 ca filtre le choix, n est pas complet si n est pas completstrainV

coveredVitamin(V) :- minCompletS(S) ; completeStrainV(S,V). %88 une vit est couverte si elle est completeStrainV
%:- not coveredVitamin(V) ; vitamin(V). %88

%#minimize {1@1,S:minCompletS(S)}.
#maximize {1@1,V:coveredVitamin(V)}.

%score(N) :- N={minCompletS(_)}.
%#minimize {N@1,N: score(N)}.  %88 S unsafe..

 %* 3 minimal set of strains having enzymes of all vitamins *%
 1{minStrain(S): strain(S)} maxstrain.  %88' choix

 coveredEnzyme(V,Ec) :- total_match(V,S,_,Ec) ;  minStrain(S) . %88
% :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) . %88'il nexiste pas denzyme non couverte?
uncovered(V,Ec) :- not coveredEnzyme(V,Ec) ; enzymeV(V,Ec) .
% #minimize {1@1,S:minStrain(S)}.
 #maximize {1@1,V,Ec:coveredEnzyme(V,Ec)}.