% Souche1, ec 1..10
num_access("Souche1","Uni1", "REFSEQ").
num_access("Souche1","Uni2", "REFSEQ").
num_access("Souche1","Uni3", "REFSEQ").
num_access("Souche1","Uni4", "REFSEQ").
num_access("Souche1","Uni5", "REFSEQ").
num_access("Souche1","Uni6", "REFSEQ").
num_access("Souche1","Uni7", "REFSEQ").
num_access("Souche1","Uni8", "REFSEQ").
num_access("Souche1","Uni9", "REFSEQ").
num_access("Souche1","Uni10", "REFSEQ").

%Souche2, ec 11..21
num_access("Souche2","Uni11", "REFSEQ").
num_access("Souche2","Uni12", "REFSEQ").
num_access("Souche2","Uni13", "REFSEQ").
num_access("Souche2","Uni14", "REFSEQ").
num_access("Souche2","Uni15", "REFSEQ").
num_access("Souche2","Uni16", "REFSEQ").
num_access("Souche2","Uni17", "REFSEQ").
num_access("Souche2","Uni18", "REFSEQ").
num_access("Souche2","Uni19", "REFSEQ").
num_access("Souche2","Uni20", "REFSEQ").
num_access("Souche2","Uni21", "REFSEQ").
%Ecs hors pathways:
num_access("Souche2","Uni22", "REFSEQ").
num_access("Souche2","Uni23", "REFSEQ").
num_access("Souche2","Uni24", "REFSEQ").
num_access("Souche2","Uni25", "REFSEQ").
num_access("Souche2","Uni26", "REFSEQ").

%Souche3, ec 6..10
num_access("Souche3","Uni6", "REFSEQ").
num_access("Souche3","Uni7", "REFSEQ").
num_access("Souche3","Uni8", "REFSEQ").
num_access("Souche3","Uni9", "REFSEQ").
num_access("Souche3","Uni10", "REFSEQ").

%taxonomie
taxonomy("Souche1","Propionibacterium","freudenreichii").
taxonomy("Souche2","Propionibacterium","fred").
taxonomy("Souche3","Prop","freudenreichii").

%Num EC des souches, 1..30
uniprot( ec(1,1,1,1),"Uni1").
uniprot( ec(1,1,1,2),"Uni2").
uniprot( ec(1,1,1,3),"Uni3").
uniprot( ec(1,1,1,4),"Uni4").
uniprot( ec(1,1,1,5),"Uni5").
uniprot( ec(1,1,1,6),"Uni6").
uniprot( ec(1,1,1,7),"Uni7").
uniprot( ec(1,1,1,8),"Uni8").
uniprot( ec(1,1,1,9),"Uni9").
uniprot( ec(1,1,1,10),"Uni10").
uniprot( ec(1,1,1,11),"Uni11").
uniprot( ec(1,1,1,12),"Uni12").
uniprot( ec(1,1,1,13),"Uni13").
uniprot( ec(1,1,1,14),"Uni14").
uniprot( ec(1,1,1,15),"Uni15").
uniprot( ec(1,1,1,16),"Uni16").
uniprot( ec(1,1,1,17),"Uni17").
uniprot( ec(1,1,1,18),"Uni18").
uniprot( ec(1,1,1,19),"Uni19").
uniprot( ec(1,1,1,20),"Uni20").
uniprot( ec(1,1,1,21),"Uni21").
uniprot( ec(1,1,1,22),"Uni22").
uniprot( ec(1,1,1,23),"Uni23").
uniprot( ec(1,1,1,24),"Uni24").
uniprot( ec(1,1,1,25),"Uni25").
uniprot( ec(1,1,1,26),"Uni26").

uniprot( ec(1,1,1,27),"Uni27").
uniprot( ec(1,1,1,28),"Uni28").
uniprot( ec(1,1,1,29),"Uni29").
uniprot( ec(1,1,1,30),"Uni30").

 %*Enzymes de pathway des vits (on simplifie le coté metacyc hein) *%
%Vitamine 1, ec 1..13
enzymeV("vit1", ec(1,1,1,1)).
enzymeV("vit1", ec(1,1,1,2)).
enzymeV("vit1", ec(1,1,1,3)).
enzymeV("vit1", ec(1,1,1,4)).
enzymeV("vit1", ec(1,1,1,5)).
enzymeV("vit1", ec(1,1,1,6)).
enzymeV("vit1", ec(1,1,1,7)).
enzymeV("vit1", ec(1,1,1,8)).
enzymeV("vit1", ec(1,1,1,9)).
enzymeV("vit1", ec(1,1,1,10)).

enzymeV("vit1", ec(1,1,1,11)).
enzymeV("vit1", ec(1,1,1,12)).
enzymeV("vit1", ec(1,1,1,13)).

%Vitamine 2, ec 14..21
enzymeV("vit2", ec(1,1,1,14)).
enzymeV("vit2", ec(1,1,1,15)).
enzymeV("vit2", ec(1,1,1,16)).
enzymeV("vit2", ec(1,1,1,17)).
enzymeV("vit2", ec(1,1,1,18)).
enzymeV("vit2", ec(1,1,1,19)).
enzymeV("vit2", ec(1,1,1,20)).
enzymeV("vit2", ec(1,1,1,21)).


%Vitamine 3, ec 27..30 enzymes pas présentes chez les bacts => insatifiable si ya le :- faux de la 3=>reglé
enzymeV("vit3", ec(1,1,1,27)).
enzymeV("vit3", ec(1,1,1,28)).
enzymeV("vit3", ec(1,1,1,29)).
enzymeV("vit3", ec(1,1,1,30)).

% définition des vitamines
vitamin("vit1").
vitamin("vit2").
vitamin("vit3").
% définition des souches => pas besoin c'est ds prog
