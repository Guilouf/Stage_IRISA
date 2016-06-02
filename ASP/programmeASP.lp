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

% todo séparer les parties test et vraies données

 %*
PARTIE test
*%
%vitamin(k2_7).
%vitamin(b9).
%vitamin(b12).

%définition du pathway, des vitamines et souches ## A commenter en test: vitamin et pathway (pas necessaire en fait)
pathwayV(V,P) :- superpathwayV(V,SPN) ; common_name(SP,SPN) ; is_a(P,SP).
vitamin(V) :- superpathwayV(V,_).
strain(S) :- num_access(S,_,_).


superpathwayV(k2_7,"superpathway of menaquinol-7 biosynthesis").
superpathwayV(b9,"superpathway of tetrahydrofolate biosynthesis").
superpathwayV(b12,"adenosylcobalamin biosynthesis I (early cobalt insertion)").


%les enzymes appartenants aux vitamines
enzymeV(V,Ec) :-    in_pathway(R,P) ;
                    ec_number(R,Ec) ;
                    not impEc(Ec) ; %'retire des enzymes selectionnées
% Ec doit être présent dans au moins une souche..boh, au final..
                    pathwayV(V,P).

%alterP(V,P_bis,R_bis)
alterP(V,P_bis,R_bis) :- in_pathway(R,P) ;
                in_pathway(R_bis,P_bis) ;
                ec_number(R,Ec) ;
                product(R, Product, _) ;
                product(R_bis, Product, _) ;
                not hidden(Product) ;
                reactant(R_bis, Reactant, _) ;
                R!=R_bis ;
                impEc(Ec) ;
                pathwayV(V,P) .




enzymeSucc(V,Ec1,Ec2) :-    in_pathway(R1,P1) ;
                    ec_number(R1,Ec1) ;
                    not impEc(Ec1) ; %'retire des enzymes selectionnées
                    in_pathway(R2,P2) ;
                    ec_number(R2,Ec2) ;
                    not impEc(Ec2) ;
                    product(R1, Product, _) ;
                    reactant(R2, Product, _) ;
                    not hidden(Product) ;
                    pathwayV(V,P1) ;
                    pathwayV(V,P2).





%les enzymes des souches qui matchent avec celles des vits, ac possib de matchs asymétriques. peut changer primaire/ref
matched(V,S,T,EcV,EcS) :-
                        enzymeV(V,EcV) ;
                        uniprot(EcS,Uniref);
                        num_access(S,Uniref,_); %888 'changer ici pour refseq !!!!!!!!
                        map(EcV,EcS,T).

%les enzymes appartenants aux souches, et correspondant aux enzymes du pathway(pareil que matched, - d'args.
enzymeS(V,S,EcS,T) :- matched(V,S,T,EcV,EcS).

%matchs asymétriques, avec exclusion des nums déja matchés en full
match_rest(V,S,T,EcV,EcSS) :- matched(V,S,T,EcV,EcSS) ; not matched(V,S,_,EcV,EcV) .

%mappeur d'EC, définit les types de relations, symétriques/asymétriques
map(ec(X,Y,Z,T),ec(X,Y,Z,T),t(4,4)) :- enzymeV(V,ec(X,Y,Z,T)).
map(ec(X,Y,Z,T),ec(X,Y,Z),t(4,3)) :- enzymeV(V,ec(X,Y,Z,T)).

map(ec(X,Y,Z),ec(X,Y,Z,T),t(3,4)) :- enzymeV(V,ec(X,Y,Z)) ; uniprot(ec(X,Y,Z,T),_).
map(ec(X,Y,Z),ec(X,Y,Z),t(3,3)) :- enzymeV(V,ec(X,Y,Z)).

%initialisation des types de correspondances et des tailles d'ec
type(t(4,4)). type(t(4,3)). type(t(3,4)). type(t(3,3)).
size_ec(ec(X,Y,Z,T),4) :- enzymeV(V,ec(X,Y,Z,T)).
size_ec(ec(X,Y,Z),3) :- enzymeV(V,ec(X,Y,Z)).

%le système de matchs
% todo faire les exclusions ailleurs?
full_match(V,S,T,Ec) :- matched(V,S,T,Ec,Ec).   % , S="FN806773".
rest_match(V,S,T,EcS) :- match_rest(V,S,T,EcS,EcC).   % , S="FN806773".
total_match(V,S,T,EcS) :- full_match(V,S,T,EcS).
total_match(V,S,T,EcS) :- rest_match(V,S,T,EcS).    %'pr tester sans spé de substrat
% todo renomer ecs en ec v..

%Les numéros Ec exclus (heu ya peut être un autre méthode..
%impEc(ec(3,7,1,12);ec(3,6,1,o);ec(1,5,1,39)).

impEc(ec(1,5,1,39)).
impEc(ec(3,6,1,o)).
impEc(ec(3,7,1,12)).

% Données metacyc supplémentaires
%enzymeV(b12, ec(2,1,1,131)).%'relativement présent'
%enzymeV(b12, ec(1,16,1,3)). %'pas présent                  !!!!!A commenter ca fait bugger sinon..





 %* Mon essai des 3 questions*%
% souches qui ont des enzymes dans ttes les vits
%strainAllPartV(S) :- total_match(V,S,T,Ec) : vitamin(V) ; strain(S).

%souches qui peuvent coopérer pour faire une vitamine (genre K)
%strainCoop(S) :- not completeStrainV(S,V) ; vitamin(V) ; strain(S) ; total_match(V,S,T,Ec) : enzymeV(_,Ec) .  %'S et V unsafe..'

 %* PARTIE SHOW*%
#show.

%#show alterP/3.


 %*Mes questions  *%
%faire des tests en retirant la spé du substrat
%#show strainAllPartV/1.  %'marche
%#show strainCoop/1.  %'aucun résultat..'

 %*Les 3 télés  *%
%#show completeStrainV/2.



 %* Tableau croisé: pr une vitamine *%
%#show enzymeV/2.
%#show full_match/4.
%#show rest_match/4.


%#show enzymeSucc/3.

%#show total_match/4.
%#show strain/1.

 %* Stats de la BDD *%
% le nombre total de souches dans la bdd (68)
%#show souche(S) : num_access(S,_,_).

% le nombre de souches dans le tableau (65)  64 pour la b9
%#show souchetab(S) : matched(V,S,T,EcV,EcS).

% les souches qui ne sont pas dans le tableau: (3) pour toutes, 4 pour b9 (NZ_LKLZ01000013.1)
%#show notab(S) : strain(S) , not matched(_,S,_,_,_).

% nombre de souches annotées d'un type ou l'autre
%#show souche(S) : num_access(S,_,"PRIMAIRE").
%#show souche(S) : num_access(S,_,"PRIMAIRE") , not num_access(S,_,"REFSEQ").

% nombre d'ec retrouvés par l'une ou l'autre des annot, par vit (changer dans le code du dessus..)
%#show typeannot(V,S,Ec) :  matched(V,S,_,Ec,_).