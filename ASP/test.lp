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

 %*
%a partir de ca on peut retrouver des reactions associés un pathway chez mes bactéries
%bon alors ce pathway n'est pas associé à une reaction.. mais certains trucs sont des instances de ce pathway..
react_path(Autrepath, Reaction_id, Uniref, Ec) :-
        in_pathway(Reaction_id, Autrepath) ;
        is_a(Autrepath, Pathway_id); %"faudrait remonter toute la hierarchie, comme en rdf"

        ec_number(Reaction_id, Ec);
        uniprot(Ec, Uniref);
        num_access(Refseq, Uniref);
        common_name(Pathway_id, "superpathway of tetrahydrofolate biosynthesis").

id_path(Pathway_id) :- common_name(Pathway_id, "superpathway of tetrahydrofolate biosynthesis").

%donc pas d'acc uniprot en commun..
uni_comun(Uniref) :- uniprot( _, Uniref) ; uniprotID(_, Uniref).

#show.

%#show react_path/4.

%cool ca marche, c'est pour montrer le nom des paths
#show nom_path(Nom): react_path(Autrepath, Reaction_id, Uniref, Ec) ; common_name(Autrepath, Nom).
%#show id_path/1.
%#show uni_comun/1.

*%

%ok on va essayer de remonter la hierarchie de is_a
%"PWY-6612", is_a: "ALL-CHORISMATE-PWY","FOLSYN-PWY"
% et "PWY-6543","PWY-6614","PWY-6147" sont des 6612.


hierarchie(I+1,Hier_inf) :- is_a(Hier_inf,Hier_sup) ; niveau(I,Hier_inf).


niveau(0,Hier_inf) :- is_a(Hier_inf, "FOLSYN-PWY").
niveau(I,Hier_inf) :- is_a(Hier_inf, Hier_sup) ; niveau(I-1,Hier_sup).


#show.
#show hierarchie/2.