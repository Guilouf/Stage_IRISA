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
*%



target(X):- is_a(X,"Menaquinols").

le_reac(Reac) :- product(Reac, X, Stoc).
numero_ec(Ec) :- ec_number(Reac, Ec).

ref_uni(Access_uni) :- uniprot( Ec,Access_uni).

#show.
%#show target/1.
% bon ca ne marche que en mettant /1...

%#show le_reac/1.
%#show numero_ec/1.
#show ref_uni/1.

