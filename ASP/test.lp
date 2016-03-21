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

 %*
 C'est sensé donner les ident uniprot de mes protéines qui ont un ec associé à une reaction ou des menaquinols sont
 produits
 *%

% selectionne un truc qui est un menaquinol
%target(X) :- is_a(X,"Menaquinols").

% selec la reaction qui produit le truc
%la_reac(Reac) :- product(Reac, X, Stoc).

% selec le numero ec de la reaction
%numero_ec(Ec) :- ec_number(Reac, Ec).

%selection une de mes l'access uniprot qui matchent ac le numero ec
ref_uni(Access_uni) :- uniprot( Ec, Access_uni).

% relie l'enzyme id a mon access uniport
uni_commun(Enzyme_id) :- uniprotID(Enzyme_id, ref_uni(Access_uni))  .

#show.
%#show target/1.
% bon ca ne marche que en mettant /1...

%#show la_reac/1.

%#show numero_ec/1.
#show ref_uni/1.
#show uni_commun/1.

