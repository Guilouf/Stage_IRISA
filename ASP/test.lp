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
% selectionne un truc qui est un menaquinol
%target(X) :- is_a(X,"Menaquinols").

% selec la reaction qui produit le truc
%la_reac(Reac) :- product(Reac, X, Stoc).

% selec le numero ec de la reaction
%numero_ec(Ec) :- ec_number(Reac, Ec).

%selection une de mes l'access uniprot qui matchent ac le numero ec
%mes_uni(Ec, Access_uni) :- uniprot( Ec, Access_uni).



% relie l'enzyme id a mon access uniport
%uni_tgdb(Enzyme_id) :- uniprotID(Enzyme_id, Access_uni)  ; uniprot( Ec, Access_uni).


%uni_tgdb(Enzyme_id, Access_uni) :- uniprotID(Enzyme_id, Access_uni).


ec_commmun(Ec, Reaction_id) :- ec_number(Reaction_id, Ec) ; uniprot( Ec, Access_uni).


%dire de ne montrer que les trucs que je veux
#show.

%#show target/1.
% bon ca ne marche que en mettant /1...

%#show la_reac/1.

%#show numero_ec/1.
%#show uniprot/2.
#show ec_commmun/2.
#show uni_tgdb/2.
#show uni_commun/1.
#show coucou(X): mes_uni(X,_).

%bon apparement ya pas de correspondance entre les acc de mes proteines et celles de tgdb..
*%

%bon alors ce pathway n'est pas associé à une reaction.. mais certains trucs sont des instances de ce pathway..
react_path(Autrepath, Reaction_id) :- in_pathway(Reaction_id, Autrepath) ;
                        is_a(Autrepath, Pathway_id); %"faudrait remonter toute la hierarchie, comme en rdf"

                        common_name(Pathway_id, "superpathway of tetrahydrofolate biosynthesis").

id_path(Pathway_id) :- common_name(Pathway_id, "superpathway of tetrahydrofolate biosynthesis").

#show.

#show react_path/2.
%#show id_path/1.