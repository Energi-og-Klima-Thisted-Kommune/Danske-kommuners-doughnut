# Akademisk gennemgang af data og metode (november 2026)

En uafhængig gennemgang af platformens data og metode, lavet 15. november 2026 på masterfilen fra commit `7ee9884`. Den bygger oven på de tidligere runder (`indikator-gennemgang-juli-2026.md`, `metode-anbefalinger-juli-2026.md`, `oekologisk-gennemgang-sep-2026.md` og de to metodeartikler) og gentager dem ikke. Fokus er på det, de runder ikke fandt, og på nye datakilder, hvor data er tynde.

Notatet er et beslutningsoplæg: hvert fund har en løsning med pris, og valgene er projektlederens. Tallene i notatet er beregnet på masterfilen, som den så ud før rettelserne.

**Status 16. november 2026.** Projektlederen har besluttet at følge anbefalingerne, bortset fra opdelingen af Forurening (afsnit 3.2), fordi de eksisterende dimensioner ikke skal ændres. Trin 1 i afsnit 6 er gennemført: S2, S3 (sygehusophold standardiseret, hjemmesygepleje fjernet), S4 (vejrskader og musikskole) og E1's niveau og grænse. De endelige tal står i `data/CHANGELOG.md` under 16. november og afviger lidt fra notatets skøn, fordi pipelinen bruger sine egne årgange og nævnere. To steder i notatet er rettet efter beslutningen, fordi jeg havde beskrevet konsekvensen forkert eller ufuldstændigt; de er mærket "Rettet 16. nov.".

**Beslutninger 16. november 2026, anden runde.** Tre spørgsmål stod åbne efter trin 1. De blev vurderet på ny med vægt på, om en kommunalbestyrelse kan læse og handle på tallet, og om det passer til Doughnut-modellens idé om en bundgrænse. Det ændrede to af notatets anbefalinger, og projektlederen har fulgt den nye vurdering:

- *Normaliseringen (S1) er udskudt.* Løsning A er statistisk renere, men "93 betyder 0,7 standardafvigelser under" kan ikke forklares i et byråd, hvor "87 betyder 13 % under landsgennemsnittet" kan. En standardiseret skala gør desuden ringen til et rent rangordningsinstrument, hvor godt en tredjedel af felterne er røde pr. konstruktion, og det trækker væk fra modellens idé om en minimumsstandard. I stedet er løsning C gennemført: de faktiske vægte beregnes ved hvert build og står ved hver indikator på metodesiden, og kategorier, hvor én indikator står for mindst to tredjedele, er mærket. De skæve vægte består.
- *Usikkerhed (S5) er gennemført for indikatorer med tidsserie:* treårsgennemsnit for kriminalitet og NEET, mærket "inden for usikkerheden" og kravet om en sikker tendens bag pilen. Stikprøveintervaller for Sundhedsprofilen mangler, fordi antallet af svar pr. kommune ikke hentes endnu.
- *Mål (S6): kun politisk vedtagne mål, der er en bundgrænse for borgernes vilkår.* Ungdomsuddannelse er på plads. Beskæftigelsesmålet på 80 % er et mål for arbejdsudbud og ikke en bundgrænse, så beskæftigelse måles fortsat mod landsgennemsnittet. NEET-målet tages først med, når udgangsåret og afgrænsningen ("unge op til 25" mod DST's 16-24-årige) er bekræftet. Partnerskabsmål bruges ikke til scoring.
- *Forbrugs-CO2 (E1): det kalibrerede 2011-mønster beholdes* og er mærket "Estimat" ved indikatoren. Forskellene mellem kommunerne er en indkomsteffekt, som er dokumenteret (Jack & Ivanova 2021; Arbejderbevægelsens Erhvervsråd 2025: 3,6 ton i laveste indkomsttiendedel mod 14,0 i højeste), og uden den ville de velstående kommuner stå grønnest i den sociale ring og som alle andre i den økologiske.

**Tilføjelse 16. november 2026: Arealanvendelse.** Efter gennemgangen spurgte projektlederen, hvorfor en kommune med 58 % antropiseret areal stod under grænsen, når den planetære grænse er 15 %. Svaret var, at dimensionen blev målt mod landsgennemsnittet. De 15 % er en global grænse og kan ikke nås i nogen dansk kommune, så de giver ingen retning. Dimensionen måler nu intensivt landbrug i procent af det ubebyggede areal mod 53,4 %, udledt af den grønne treparts vedtagne mål om at omlægge ca. 10 % af Danmarks areal frem mod 2045. Det følger samme princip som de sociale mål: kun politisk vedtagne grænser. Dimensionens navn er uændret. Regnestykke og forbehold står på metodesiden og i `data/CHANGELOG.md`; tabellen i afsnit 3 beskriver stadig den gamle indikator.

Vejen til flere absolutte mål i den sociale ring går efter denne vurdering gennem kommunens egne vedtagne mål, som DEAL's byportrætter gør. Det er ikke undersøgt her.

**Sådan er påstandene mærket.** *Beregnet* betyder, at tallet kommer fra `docs/gennemgang-nov-2026/analyse.py`, som læser de committede datafiler og kan køres igen. *Kilde* betyder, at oplysningen er set på kildens egen side under gennemgangen, og adressen står i afsnit 5 eller 8. *Vurdering* er min fortolkning. *Ikke bekræftet* betyder, at jeg mener oplysningen er rigtig, men ikke har kunnet se den hos kilden, og den skal tjekkes før brug.

## 1. Kort fortalt

De tidligere runder har ryddet op i indikatorvalget og i den økologiske rings grænser. Det, der står tilbage, ligger et lag dybere: i hvordan en råværdi bliver til en score, og i hvor sikkert tallet er. Otte fund ændrer efter min vurdering, hvad platformen kan sige med faglig dækning.

| # | Fund | Konsekvens i dag (beregnet) | Løsning | Pris |
|---|---|---|---|---|
| S1 | Ratio til referencen giver indikatorerne vidt forskellig vægt, og vægten afhænger af, om tallet er formuleret positivt eller negativt | I Sundhed bærer middellevetid 1 % og selvvurderet helbred 3 % af kategoriens variation; hjemmesygepleje, rygning, kost og overvægt hver 21-24 %. I Mobilitet (standardvisning) bærer kollektiv transport 94 % | Standardiseret afstand til referencen for relative indikatorer; komplementformel for mål | Ændrer alle sociale scorer. Arkitekturbeslutning |
| S2 | Uddannelses to niveauindikatorer er samme tal i to aldersgrupper, og 95 %-målet er mærket forkert | `education` og `low_education` korrelerer -0,85 og har tilsammen 47 % af kategoriens vægt | Én indikator, målt mod det gældende mål for ungdomsuddannelse | Lille |
| S3 | Rå rater måler aldersstruktur | Aldersstandardisering skifter farve for 24 kommuner på sygehusophold og 34 på hjemmesygepleje; Ærø går fra 63 til 106 | Standardisér de to (data findes i samme DST-tabeller); afklar Sundhedsprofilen | Lille for de to registerindikatorer |
| S4 | Flere rater deles med indbyggere, hvor de udsatte er noget andet | Vejrskader pr. indbygger følger andelen af fritidshuse (0,59); Odsherred går fra 66 til 150 pr. boligenhed. Musikskole pr. barn skifter 17 farver | Ret nævneren | Lille |
| S5 | Platformen viser ingen usikkerhed, og den er stor nogle steder | Tryghed: standardfejl 7 point, 86 af 98 farver i standardvisningen ligger inden for usikkerheden af en farvegrænse. Sundhedsprofilens tal har ±13-29 scorepoint i en kommune med minimumsstikprøven. 18 % af de vurderede pile har ingen statistisk sikker tendens | Glidende gennemsnit, mærket "ikke forskellig fra referencen", og krav om tendens bag pilen | Mellem |
| S6 | 45 af 47 sociale indikatorer er relative, selv om der findes vedtagne mål for flere | Ringen kan ikke vise, om et mål er nået. Politisk vedtagne mål findes for ungdomsuddannelse, NEET og beskæftigelse; partnerskabsmål for ensomhed og rygning | Mål de tre første mod målet; beslut om partnerskabsmål skal bruges | Lille pr. indikator |
| E1 | Forbrugs-CO2 ligger på et niveau, ingen af kilderne står bag, mønstret er en indkomstfordeling fra 2011, og grænsen gælder kun husholdningernes del | Platformens tal giver 11,3 ton pr. dansker mod Energistyrelsens 9,7 for samme år. Tallet afgør klimadimensionen i 87 kommuner. Der findes ingen nyere kommunetal | Kalibrér niveauet; lad grænse og tal dække det samme (3 ton har en kilde); beslut om mønstret skal scores | Lille for niveau og grænse |
| E2 | Tre dimensioner måler noget andet, end navnet og grænsen siger | Forurening er et gennemsnit af fire ukorrelerede tal; Biodiversitet måler naturværdi mod et mål for beskyttet areal; Luftkvalitet kan ikke skelne kommuner | Se afsnit 3 | Varierer |

Min anbefaling til rækkefølge står i afsnit 6. S2, S3, S4 og niveauet i E1 er fejl eller nær-fejl, som kan rettes uden at røre arkitekturen. S1 og S5 er de to, der betyder mest for den faglige kvalitet, og de kræver en beslutning om, hvordan platformen skal læses.

## 2. Den sociale ring

### 2.1 Normaliseringen bestemmer vægtene (S1)

**Fund (beregnet).** En social score er værdi/reference × 100, eller den vendte brøk når lavt er godt. En kategori er gennemsnittet af sine scorer, og artikel 1 skriver, at alle indikatorer i en kategori vejer lige meget. Det gør de kun i regnestykket. En indikators bidrag til forskellene mellem kommuner er proportionalt med dens relative spredning (variationskoefficienten), og den varierer med en faktor 50 mellem indikatorerne.

| Kategori | Nominel vægt | Faktisk andel af kategoriens varians (landsgennemsnit / kommunegruppe) |
|---|---|---|
| Sundhed (9) | 11 % hver | middellevetid 1 / 1, selvvurderet helbred 3 / 4, mentalt helbred 5 / 13, sygehusophold 7 / 8, hjemmesygepleje 24 / 16, rygning 22 / 24, kost 21 / 20, svær overvægt 22 / 19, alkohol -4 / -4 |
| Uddannelse (8) | 12,5 % hver | unge med kun grundskole 40 / 34, højt fravær 36 / 40, uddannelse mod 95 % 6 / 6, karakterer 7 / 6, trivsel 2 / 2, klassekvotient -2 / 3 |
| Velfærd (7) | 14 % hver | beskæftigelse 3 / 3, børnefattigdom 23 / 25, udsatte børn 22 / 21 |
| Mobilitet (2) | 50 % hver | kollektiv transport 71 / 94, pendling 29 / 6 |
| Lighed (2) | 50 % hver | Gini 73 / 77 |
| Ligestilling (3) | 33 % hver | indkomstlighed 5 / 6 |
| Demokrati (2) | 50 % hver | kommunalvalg 70 / 68 |

En negativ andel betyder, at indikatoren trækker modsat resten af kategorien (alkohol, som artikel 1 også nævner).

Den dybere svaghed er, at vægten afhænger af, hvordan tallet er formuleret. Selvvurderet helbred står som andelen med godt helbred (82 %), og de øvrige Sundhedsprofil-tal står som andelen med et problem (10-20 %). De samme svar formuleret som "ikke godt helbred" (18 %) ville give en spredning på 15 point i stedet for 3, og 17 kommuner under 85 i stedet for ingen. Tilsvarende for beskæftigelse (0 mod 3 under 85), forventet ungdomsuddannelse (0 mod 32) og valgdeltagelse ved folketingsvalg (0 mod 13). En metode bør give samme svar, uanset om man tæller dem, der har, eller dem, der mangler.

De to ringe behandler desuden samme situation forskelligt. Den økologiske ring regner mål for andele som den manglende andel mod det, målet tillader (R2a, komplementformlen). Den sociale ring regner uddannelsesmålet som andel/95. Med den sociale formel har 19 kommuner rød uddannelse; med den økologiske rings logik har ingen kommune nået målet, og medianen mangler 3,2 gange så meget, som målet tillader.

Tre følger af samme rod er allerede kendt i projektet, men behandlet hver for sig: loftet på 150 (nødvendigt, fordi den vendte brøk vokser uden grænse), "dekorations"-indikatorerne med lav spredning (middellevetid, trivsel), og at farvegrænsen 85 er uopnåelig i nogle kategorier og almindelig i andre. Demokrati har ingen røde kommuner og Uddannelse én, mens Mobilitet har 63, og forskellen skyldes kategoriernes spredning (5 mod 37 point), ikke at mobiliteten er et større problem end uddannelsen.

**Litteratur.** Forskellen mellem nominelle vægte og indikatorernes faktiske betydning er et kendt problem i sammensatte indikatorer (Paruolo, Saisana & Saltelli 2013; Becker m.fl. 2017). OECD/JRC-håndbogen (2008) behandler "afstand til reference" som én af flere normaliseringer og anbefaler at teste følsomheden over for valget.

**Løsninger.**

- *A. Standardiseret afstand til referencen.* Score = 100 + 10 × (værdi − reference) / standardafvigelsen mellem kommunerne, med fortegnet vendt når lavt er godt, og klippet ved tre standardafvigelser. 100 er stadig referencen. Skalaen er den, Mazziotta & Pareto (2016) bruger. Den giver samme svar for "har" og "mangler", gør lige vægte reelle (i Velfærd 12-16 % pr. indikator mod 3-25 % i dag), er symmetrisk om referencen og gør loftet på 150 overflødigt. Beregnet konsekvens: rangkorrelationen med de nuværende kategoriscorer er 0,96-0,99 i Sundhed, Velfærd, Demokrati, Kultur, Tryghed og Klimatilpasning, og 0,89-0,93 i Ligestilling, Uddannelse, Fællesskab og Mobilitet, hvor 10-17 kommuner flytter mere end 20 pladser. Prisen er, at tallet ikke længere kan læses som "procent af landsgennemsnittet", og at standardafvigelsen skal fastfryses i et basisår, hvis scoren skal kunne sammenlignes over tid. Farvegrænserne skal sættes på ny (fx én standardafvigelse under referencen).
- *B. Behold ratioen, men formulér alle andele som mangel.* Alle andele vendes, så de tæller dem, der er under en standard, som Fanning & Raworth (2025) gør. Det fjerner afhængigheden af formuleringen for andele, men ikke forskellen mellem enheder (år, kroner, karakterer), og det øger afhængigheden af loftet.
- *C. Behold metoden og offentliggør de faktiske vægte.* Tabellen ovenfor på metodesiden og i artikel 1, og "vejer lige meget" rettes til "indgår med lige vægt i gennemsnittet; den faktiske betydning følger spredningen". Løser intet, men er ærligt.

Min anbefaling er A for de relative indikatorer og komplementformlen for de indikatorer, der måles mod et mål (S6), så de to ringe følger samme logik. C bør under alle omstændigheder gøres nu. Valget mellem A og B er en arkitekturbeslutning, og den hænger sammen med S5: en standardiseret skala gør det også lettere at vise usikkerhed.

### 2.2 Uddannelse tæller samme tal to gange (S2)

**Fund (beregnet og læst i koden).** `education` henter DST HFUDD11 for 30-34-årige med koderne H20 (gymnasial), H30, H35 og H40-H80, altså alle med mere end grundskole. `low_education` er 25-29-årige med kun grundskole. De to er hinandens komplement i to nabo-aldersgrupper: de korrelerer -0,85, og summen af de to andele er 104,6 med en spredning på 3,0. Den tidligere regel om at slå indikatorer med r over 0,7 sammen fangede det ikke. Tilsammen bærer de 47 % af variationen i Uddannelse.

`education` hedder "Kompetencegivende uddannelse", og registret begrunder målet med "95 % skal have erhvervskompetencegivende uddannelse". En gymnasial uddannelse er ikke erhvervskompetencegivende, så navnet passer ikke til det, der tælles. 95-procent-målsætningen gjaldt ungdomsuddannelse: mindst 95 % af en ungdomsårgang skulle gennemføre en ungdomsuddannelse, målt med profilmodellen 25 år efter 9. klasse (aftale om globaliseringspuljen 2006; Rigsrevisionen 2012). Den blev i efteråret 2017 erstattet af målet om, at mindst 90 % af en årgang skal have gennemført en ungdomsuddannelse, inden de fylder 25 år (Rigsrevisionen 2019). Danmarks Statistik regner kun hovedgrupperne 30-80 som erhvervskompetencegivende. Indikatoren tæller altså det, målet handlede om (ungdomsuddannelse), men under et forkert navn, i en anden aldersgruppe end målet og mod et mål, der er afløst. (Kilde for alle fire oplysninger, se afsnit 8.)

**Løsning.** Behold én indikator for uddannelsesniveau, kald den det, den måler (mindst en ungdomsuddannelse), og mål den mod det gældende mål. Det er 90 % af de 25-årige med gennemført ungdomsuddannelse. Målåret er 2030 ifølge KL og Reformkommissionen, som begge gengiver aftalen fra oktober 2017; selve aftaleteksten kunne ikke åbnes hos ministeriet (se 2.6). Fjern den anden, eller erstat den med et tal, der måler noget andet. Efter 2.1 bør målet regnes med komplementformlen.

Der er et bredere mønster her. Forventet ungdomsuddannelse korrelerer 0,85 med medianindkomsten og karaktergennemsnittet 0,79. Rå karakterer måler i høj grad forældrenes baggrund. Børne- og Undervisningsministeriet udgiver en socioøkonomisk reference for karakterer, som viser, om eleverne klarer sig bedre eller dårligere end elever med samme baggrund på landsplan. Det tal ville måle skolens bidrag frem for kommunens sammensætning. *Ikke bekræftet:* at referencen kan hentes pr. kommune fra det API, `fetch_udvidelse_data.py` allerede bruger.

### 2.3 Rå rater måler aldersstruktur (S3)

**Fund (beregnet).** Andelen af borgere på 65 år og derover går fra 11 % (København) til 43 % (Læsø). Ingen af sundhedsindikatorerne er aldersstandardiseret, bortset fra middellevetiden, som er det i sin konstruktion. Kommunens aldersfordeling alene (andel 0-19, 65+ og 80+) forklarer 74 % af variationen i hjemmesygepleje og 45 % i sygehusophold.

De to DST-tabeller har alder som variabel, så jeg har regnet de standardiserede tal: direkte standardisering til landets aldersfordeling for sygehusophold (SBR01, 19 aldersgrupper) og observeret mod forventet antal ved landets aldersrater for hjemmesygepleje (HJEMSYG, 7 aldersgrupper).

| Indikator | Farver rå (grøn/gul/rød) | Farver standardiseret | Farveskift | Største ændringer i score |
|---|---|---|---|---|
| Sygehusophold 12+ timer | 36/53/9 | 48/46/4 | 24 | Læsø 78 → 112, Samsø 82 → 113, Langeland 95 → 125, København 110 → 97 |
| Hjemmesygepleje | 35/19/44 | 43/32/23 | 34 | Ærø 63 → 106, Hørsholm 86 → 125, Læsø 42 → 74, Ishøj 125 → 99 |

I Sundhed samlet skifter 11 kommuner farve i landsgennemsnitsvisningen og 7 i standardvisningen. Kommunegrupperne opfanger altså en del af aldersforskellen, men ikke den inden for grupperne (Hørsholm og Ishøj er begge hovedstadskommuner).

For de seks Sundhedsprofil-indikatorer i Sundhed og de to i Fællesskab kan jeg ikke regne standardiserede tal, fordi kommunetallene ikke er hentet opdelt på alder. Selvvurderet helbred falder med alderen, og rygning, alkohol og mentalt helbred har hver sin aldersprofil, så de er påvirket i ukendt omfang og retning. Kilden sætter en grænse for, hvad der kan gøres (kilde): databasen på danskernessundhed.dk giver pr. kommune den rå procent, antal svarpersoner og en køns- og aldersjusteret odds ratio mod landet, men ingen aldersstandardiserede andele, og vejledningen siger, at kommunetal ikke kan opdeles på alder. Odds ratioen er derfor den eneste åbne vej til et alderskorrigeret tal. Den kan regnes om til en justeret andel med landsandelen som udgangspunkt (justeret andel = OR × p / (1 − p + OR × p), hvor p er landsandelen). Det er mit forslag og er ikke afprøvet mod kilden. Alternativet er mikrodata fra NATSUP, som koster et gebyr fra 15. november 2026.

**Litteratur.** Aldersstandardisering er standard, når helbred sammenlignes mellem befolkninger med forskellig alderssammensætning (Ahmad m.fl. 2001).

**Løsning.** Standardisér `hospital_long` og `hjemsyg` i fetch-scripterne; metoden står i `analyse.py`, afsnit 6, og kræver kun, at aldersvariablen hentes med. Der er dog et spørgsmål før det for hjemmesygepleje: efter standardisering er det, der står tilbage, en blanding af sygelighed og kommunens visitationspraksis, og det er ikke klart, at færre modtagere er bedre. Det er samme tvivl, som fik `medicin` fjernet. Jeg ville fjerne indikatoren og standardisere sygehusopholdene.

Aldersfordelingen forklarer også meget af andre indikatorer (vejrskader 56 %, kollektiv transport 56 %, valgdeltagelse ved kommunalvalg 43 %). Her er alderen en markør for kommunetypen og ikke en fejlkilde i sig selv, med vejrskaderne som undtagelse (2.4).

### 2.4 Nævnere (S4)

**Fund (beregnet).** Tre indikatorer deles med folketallet, selv om de udsatte er en anden størrelse.

- *Vejrskader pr. 1.000 indbyggere.* Skaderne sker på bygninger, også fritidshuse, men deles med de fastboende. Rangkorrelationen med andelen af fritidshuse er 0,59. Delt med boliger og fritidshuse falder den til 0,30, og 15 kommuner skifter farve: Odsherred går fra 66 til 150, Fanø fra 33 til 87, Læsø fra 40 til 88 og Gribskov fra 88 til 122, mens Egedal, Allerød og Favrskov falder 20-26 point. Bolig- og fritidshustallene er her taget fra søsterprojektet forbrugsudledninger (DST BOL105) og dækker ikke erhvervsbygninger, så tallene viser retningen, ikke den endelige indikator.
- *Musikskoleelever pr. 1.000 indbyggere.* Eleverne er børn og unge. Delt med de 0-19-årige skifter 17 kommuner farve.
- *Tilskadekomne i trafikken pr. indbygger.* Ulykker registreres, hvor de sker, og følger gennemkørende trafik og sommertrafik (rangkorrelation med fritidshusandel 0,55). Her findes ingen oplagt bedre nævner pr. kommune; trafikarbejde ville være den rigtige. Det bør stå som forbehold.

**Løsning.** Del vejrskader med antal boliger og fritidshuse (DST BOL105 eller BBR) og musikskoleelever med antal børn og unge. Begge er små ændringer i fetch-scripterne og i registrets enhed.

*Rettet 16. nov.:* ved gennemførelsen har jeg sammenlignet tre nævnere for vejrskader. Pr. indbygger følger tallet andelen af fritidshuse (+0,63). Pr. bygning vender skævheden og følger andelen af etagebyggeri (+0,55), så København og Frederiksberg får tre til fire gange landstallet. Pr. bolig og fritidshus følger bygningstyperne mindst (+0,29 og -0,22) og er valgt, men den er ikke neutral: lejligheder har færre vejrskader pr. bolig end huse. Tabellen står i `data/klimatilpasning.md`. Musikskoleeleverne er afgrænset til 0-24 år i både tæller og nævner.

### 2.5 Usikkerhed (S5)

**Fund (beregnet).** Artikel 1 konstaterer, at platformen ikke viser usikkerhed. Jeg har målt den for de 36 indikatorer, der har en tidsserie på mindst seks år: støjen er spredningen om kommunens egen lineære udvikling over de seneste otte år, efter at årets fælles niveau er trukket fra. Det er et mål for, hvor meget en kommunes tal flytter sig fra år til år uden at være en del af en tendens.

- For de fleste indikatorer er støjen lille i forhold til forskellene mellem kommunerne (reliabilitet over 0,9 for 22 af 36). Lavest ligger kønsgab i middellevetid (0,74), kriminalitet, trivsel og fravær (0,82), trafikulykker (0,83) og NEET (0,84).
- Støjen er typisk to til tre gange større i kommuner under 25.000 indbyggere end i kommuner over 50.000.
- For 13 indikatorer ligger mindst 40 af 98 kommuner så tæt på referencen, at afstanden er mindre end 1,96 gange kommunens egen støj.
- På kategoriniveau er standardfejlen 7 point i Tryghed og 2,5 i Ligestilling. I standardvisningen ligger 86 af 98 Tryghedsfarver og 62 af 98 Ligestillingsfarver inden for usikkerheden af en farvegrænse. Samlet gælder det mindst 389 af 1.274 kategorifarver (31 %) i standardvisningen og 253 (20 %) mod landsgennemsnittet.

Tallene er en nedre grænse. Stikprøveusikkerheden i Sundhedsprofilens otte indikatorer er ikke med, og heller ikke de 11 indikatorer uden tidsserie. For Sundhedsprofilen kan stikprøveusikkerheden skønnes (kilde for stikprøven, beregning min). Hver kommune har mindst 2.000 inviterede, svarprocenten i 2025 var 43,0, og på Læsø var 713 inviteret, hvilket giver ca. 290 svar. Med 900 svar, som er niveauet i en kommune med minimumsstikprøven, er 95 %-intervallet for de negativt formulerede indikatorer ±13 til ±29 scorepoint, og mellem 32 og 83 af de 98 kommuner kan ikke skelnes fra landstallet, afhængigt af indikatoren. Reliabiliteten er 0,50 for begrænset social støtte, 0,66 for ensomhed og 0,69 for mentalt helbred. Med 290 svar er intervallet ±23 til ±50 point. Beregningen antager simpel tilfældig udvælgelse; vægtningen for bortfald gør den reelle usikkerhed større. Kildens vejledning nævner ingen konfidensintervaller pr. kommune, så platformen må regne dem selv af procent og antal svar, som begge kan hentes.

Retningspilene har samme svaghed. Af de 2.849 pile med en vurdering (rigtig, tempo, forkert) på serier med mindst otte år har 520 (18 %) ingen statistisk sikker monoton tendens (Mann-Kendall, p under 0,10). For børnefattigdom er kun 18 % af pilene sikre, for affald 49 % og for kønsgab i middellevetid 54 %.

**Litteratur.** Sammenligning af enheder af meget forskellig størrelse uden usikkerhed er det klassiske problem ved ranglister (Goldstein & Spiegelhalter 1996). Spiegelhalter (2005) foreslår kontrolgrænser, der afhænger af enhedens størrelse. Det engelske deprivationsindeks trækker små områders tal mod gennemsnittet (McLennan m.fl. 2019), samme greb som platformen allerede bruger for pesticider.

**Løsninger.** Fire greb, som kan tages hver for sig.

1. *Glidende gennemsnit for de støjende rater.* Kriminalitet er ét år; tre år ville halvere støjen efter samme model som trafikulykker. Det samme gælder NEET og fravær.
2. *En fjerde tilstand: "ikke forskellig fra referencen".* Når afstanden til referencen er mindre end 1,96 gange kommunens egen støj, vises indikatoren neutralt. Støjen kan regnes i `build_trends_csv.py` af den tidsserie, der allerede hentes, og skrives i `noegletal.json` ved siden af "få tilfælde" (R16). Det afløser ikke farverne, men det fjerner den falske præcision ved 99 mod 101.
3. *Stikprøveintervaller for Sundhedsprofilen.* Hent antal svar sammen med procenten, regn intervallet, og brug samme neutrale mærke. For de mindste kommuner bør tallet trækkes mod landstallet med empirisk Bayes, som pesticiderne.
4. *Pilen kræver en tendens.* En pil med vurdering vises kun, når Mann-Kendall-testen (Mann 1945) finder en tendens; ellers "ingen klar tendens". Reglen "rigtig mod tempo" efter medianen kan blive, men bør have samme krav.

### 2.6 Flere absolutte mål (S6)

**Fund (kilde).** Artikel 1 forsvarer det relative fundament med, at de globale tærskler er nået i Danmark, og nævner, at flere indikatorer kunne måles mod et mål, "hvis et sådant blev vedtaget". Der findes flere vedtagne mål, end platformen bruger. De har forskellig status, og det skal fremgå, hvis de bruges.

| Indikator | Mål | Hvem står bag | Kan bruges pr. kommune? |
|---|---|---|---|
| Uddannelsesniveau (`education`) | Mindst 90 % af de 25-årige har gennemført en ungdomsuddannelse i 2030 | Politisk aftale, oktober 2017 (regeringen, DF, S, SF, R) | Ja. Afløser det mål, platformen bruger i dag (2.2) |
| NEET (`neet`) | Andelen af unge op til 25 år uden tilknytning til uddannelse eller arbejde halveres i 2030 | Samme aftale | Ja, hvis udgangsåret fastlægges. *Ikke bekræftet:* baseline for halveringen |
| Beskæftigelse (`employment`) | 80 % af de 20-64-årige i 2030 | Regeringens nationale mål under EU's sociale søjle (2022). EU's eget mål er 78 % | Ja, men platformen måler 16-64-årige i RAS200; aldersgruppen skal følge målet |
| Ensomhed (`ensomhed`) | Halvering inden 2040: fra 8,3 % (2017) til ca. 4 % blandt personer over 16 år | Det Nationale Partnerskab mod Ensomhed, 2023. Ikke regering eller Folketing | Ja. Målet er defineret på Sundhedsprofilens skala. Afklar, at platformens afgrænsning er den samme som partnerskabets |
| Rygning (`rygning`) | Højst 5 % voksne rygere i 2030 | Partnerskabet Røgfri Fremtid (Kræftens Bekæmpelse og TrygFonden). Regeringens eget mål gælder kun børn og unge | Ja, men som partnerskabsmål |
| Trafik (`traffic_accidents`) | Højst 90 dræbte og 900 alvorligt tilskadekomne i 2030 | Færdselssikkerhedskommissionen | Nej. Landstal i antal, og platformen tæller alle tilskadekomne |
| Fattigdom | Verdensmål 1.2: halvering efter nationale definitioner i 2030 | FN. Danmark har ingen officiel fattigdomsgrænse; DST's indikatorer er udtrykkeligt ikke en grænse | Nej, ikke uden et valg af definition og basisår |
| Alkohol, fravær, trivsel, karakterer, valgdeltagelse, kriminalitet | Ingen kvantitative mål fundet | | Nej |

**Løsning.** Uddannelse bør skifte til 90 %-målet under alle omstændigheder. Beskæftigelse og NEET kan måles mod politisk vedtagne mål og giver den sociale ring fire absolutte indikatorer i stedet for to. Ensomhed og rygning kan måles mod partnerskabsmål, hvis platformen vil; så skal mærket "mod mål" skelne mellem politisk vedtagne mål og mål fra partnerskaber, ellers blandes to slags autoritet. Regnet med komplementformlen (2.1) for andele, hvor højere er bedre, og værdi/mål hvor lavere er bedre. Hvor mange kommuner der så bliver røde, har jeg ikke regnet; det bør gøres, før valget træffes.

### 2.7 Kommunegruppen som reference

**Fund (beregnet).** To mindre ting, som bør stå i arkitekturdokumentet.

- Storbygruppen har tre kommuner (Odense, Aarhus, Aalborg). Hver er en tredjedel af sin egen reference, og deres scorer trækkes mod 100: den gennemsnitlige afstand til 100 er 8,6 point med kommunen selv i snittet og 12,1 uden. I de øvrige grupper er forskellen under 1 point. Det flytter kun 2 af 39 farver, men gruppen er for lille til at være en reference. Storbyerne kunne sammenlignes med provinsbykommunerne og sig selv, eller vises mod landsgennemsnittet som standard.
- Gruppesnittet tages af de færdige scorer og ikke af råværdierne (R10 kalder det en bevidst forenkling). For vendte indikatorer er det ikke det samme. Med gruppens rå gennemsnit som reference skifter 91 af 1.274 kategorifarver (7 %), flest i Bolig (19) og Tryghed (16). Ingen af de to er forkert, men valget er ikke neutralt. Med løsning A i 2.1 forsvinder forskellen, fordi skalaen er lineær.

En vurdering: kommunegrupper er en grov korrektion for vilkår. Alternativet i litteraturen er en forventet værdi beregnet ved regression på strukturelle vilkår, som ministeriets socioøkonomiske reference for karakterer. Det er mere præcist og langt sværere at forklare. Jeg ville blive ved grupperne.

### 2.8 Tynde kategorier og nye kilder

Fem kategorier har én eller to indikatorer, og artikel 1 viser, at de er skrøbelige. For hver har jeg undersøgt, om der findes åbne data for alle 98 kommuner. Detaljer og adresser står i afsnit 5.

- **Bolig (1 indikator).** Boligbyrde findes ikke pr. kommune (DST's SILC-tabeller er landstal, huslejeindekset kun for kommunegrupper). Det, der findes, er Landsbyggefondens husleje pr. m² i almene boliger (kun almene, et niveau og ikke en byrde), VIVE's hjemløsetælling 2026 (alle kommuner, men meget små tal: Thisted 18, Morsø 6, Læsø 1) og DST's tvangsauktioner og boligstøtte. Ingen af dem er et godt andet mål. Min vurdering: lad Bolig stå med én indikator, og sig det, frem for at tilføje et svagt tal.
- **Tryghed (2).** Justitsministeriets Tryghedsundersøgelse 2023 har andelen, der føler sig tryg i nabolaget, for alle 98 kommuner. Den ville give kategorien det udfaldsmål, den mangler. Forbehold: ca. 200 svar pr. kommune, kun PDF, og ingen nyere udgave er fundet. STRAF11 kan opdeles på voldsforbrydelser og indbrud i beboelse, som er tættere på tryghed end alle anmeldelser samlet.
- **Demokrati (2).** DST LIGEDB2 og LIGEDI2 har opstillede og valgte kandidater efter køn for kommunalvalgene 2005-2025. Kvindeandelen blandt valgte hører dog bedre hjemme under Ligestilling.
- **Mobilitet og "netværk".** Raworths dimension om netværk har ingen digital indikator. DST LABY51 har andelen af boliger med adgang til hurtigt fastnetbredbånd for alle kommuner, 2014-2025.
- **Velfærd og arbejde.** DST AULK04 har langtidsledighed og SYGEDP01 sygedagpenge for alle kommuner. Begge følger den socioøkonomiske linje, som Velfærds syv indikatorer allerede følger, så de tilfører lidt.
- **Sundhed.** Sundhedsdatastyrelsens register over udvalgte kroniske sygdomme har aldersstandardiserede rater pr. kommune for ni sygdomme (bl.a. KOL, type 2-diabetes, demens), opdateret årligt. Det er et registerbaseret, allerede standardiseret alternativ til en del af Sundhedsprofilen og ville mindske afhængigheden af én spørgeskemaundersøgelse. *Ikke bekræftet:* downloadformat og diskretionering, fordi esundhed.dk ikke svarede under gennemgangen.
- **Ekstern validering.** Indenrigs- og Sundhedsministeriets socioøkonomiske indeks pr. kommune står i "Kommunerne 2026", tabel 3.2. Det kan bruges til at teste, om ringen måler mere end udgiftsbehov. Kriterierne overlapper platformens egne indikatorer, så en høj korrelation er forventet og ikke i sig selv en validering.

## 3. Den økologiske ring

Septembergennemgangen flyttede 11 af 15 indikatorer over på faste grænser, og artikel 2 gennemgår de svagheder, der blev tilbage. Her er kun det, de ikke dækker.

### 3.1 Forbrugsbaseret CO2 (E1)

**Fund.**

- *Niveauet (beregnet).* Estimatet er Osei-Owusu m.fl.s kommunetal for 2011 ganget med udviklingen i Energistyrelsens nationale tal. Metodenoten gør det med vilje for ikke at blande to modellers niveauer, men resultatet beholder Osei-Owusus niveau (15,7 ton i 2011 mod Energistyrelsens 13,5). Det befolkningsvægtede gennemsnit af platformens kommunetal er 11,3 ton pr. person, og Energistyrelsens tal for samme år er 9,7. Platformen mærker altså tallet "ENS Global Afrapportering", men ligger 16 % over den. Da tallet måles mod en fast grænse, går forskellen direkte i scoren.
- *Mønstret (beregnet).* Forskellene mellem kommuner er fra 2011 og korrelerer 0,73 med medianindkomsten i 2024. Indikatoren er i praksis en indkomstindikator med modsat fortegn af Velfærd, og en kommune kan ikke flytte den.
- *Grænsen (kilde).* De 2,5 ton er Hot or Cool-rapportens mål for 2030 for husholdningernes forbrug alene; rapporten udelader udtrykkeligt offentligt forbrug og investeringer (Akenji m.fl. 2021, s. 41). Platformens tal omfatter alt. Projektet kender forbeholdet (beslutning 25. sep. 2026), men det er ikke sat på tal; det er det nedenfor. Det territoriale tal har ingen fælles afgrænsning med målet. Til sammenligning bruger O'Neill m.fl. (2018) 1,61 ton CO2 pr. person om året for det samlede forbrugsaftryk (kun CO2, budget for 2 grader).
- *To platforme, to svar (læst i koden).* Søsterprojektet forbrugsudledninger har fjernet sit kommunale aftryk i ton, fordi ingen af koefficienterne kunne kildebelægges (`pipeline/constants.py`), og viser i stedet de målte drivere mod landet. Doughnutten scorer et kommunalt aftryk i ton, som afgør klimadimensionen i 87 af 98 kommuner. De to platforme har samme ophav og bør ikke sige hver sit om, hvad man kan vide.

**Findes der nyere data? (kilde)** Nej. Sanderson m.fl. (2024) skriver, at der ikke findes solide skøn over kommunale forbrugsbaserede udledninger i Danmark; Klima- og Omstillingsrådet brugte i september 2025 stadig 2011-kortet; og KL's arbejde med en standard og et værktøj er ifølge KL's vidensbank (juni 2026) ikke udgivet. NIRAS' rapport for CONCITO og C40 (2024) er en metodeanbefaling uden kommunetal. DST har intet på kommuneniveau. Det eneste kildebelagte grundlag for at opdatere mønstret er indkomstelasticiteten på ca. 0,5 for danske husholdningers aftryk (Jack & Ivanova 2021), som selv bygger på data fra 2010.

**Grænsen igen (kilde).** To oplysninger ændrer grundlaget for beslutningen fra 25. september:

- Energistyrelsens datafil for 2024 deler aftrykket op: husholdninger 59,9 %, investeringer 28,2 %, offentligt forbrug 11,9 %. Husholdningernes del er altså ca. 5,8 ton pr. person, og det er det tal, de 2,5 ton er lavet til at blive holdt op mod.
- De 3 ton, som blev opgivet, fordi tallet ikke havde en kilde, har én. Klimarådets baggrundsnotat om forbrugsaftrykket (november 2023) gengiver Klima- og Omstillingsrådets målsætning om 3 ton CO2e pr. indbygger i 2030 for det samlede forbrugsaftryk (lavrisiko; 6 ton er højrisiko) og CONCITO's henvisning til, at forbrugsudledningen pr. verdensborger bør under 3 ton i 2030. Klimarådet selv anbefaler et pejlemærke på 3,9-4,9 ton i 2035 for hele aftrykket. Jeg har set Klimarådets gengivelse, ikke Klima- og Omstillingsrådets egen publikation. Hot or Cool har desuden revideret sine egne mål i 2025 (1,1 ton i 2035 for livsstilsaftrykket).

Septembernotatet siger, at man kun bør gå tilbage til 3 ton, hvis nogen finder en kilde. Det er sket, og 3 ton har den fordel, at tallet gælder samme afgrænsning som det, platformen måler. Ingen farver afhænger af valget.

**Løsninger.**

1. *Kalibrér niveauet nu.* Gang kommunetallene med 9,73/11,33, så de 98 kommuner samlet giver Energistyrelsens tal. Spændet bliver 8,1-14,9 ton i stedet for 9,4-17,4. Ingen farver skifter (alle er røde), men tallet passer med den kilde, det henviser til.
2. *Lad grænse og tal dække det samme.* Enten 3 ton for det samlede aftryk med Klima- og Omstillingsrådet som kilde (efter at dens egen publikation er slået op), eller 2,5 ton holdt op mod husholdningernes del alene. Det første er enklest og følger septembernotatets egen betingelse.
3. *Beslut, om mønstret skal scores.* Tre muligheder: (a) behold det som i dag med forbeholdet; (b) scor forbrugsaftrykket som landstallet for alle kommuner, og vis 2011-mønstret som kontekst, så dimensionens forskelle mellem kommuner kommer fra de territoriale udledninger, som er målt og har en pil; (c) erstat tallet med en visning af driverne fra forbrugsudledninger (biler, boligareal, opvarmning, affald), som ikke kan måles mod 2,5 ton og derfor kun kan være kontekst. Min anbefaling var (b). *Rettet 16. nov.:* jeg skrev, at dimensionens forskelle mellem kommuner så ville komme fra de territoriale udledninger, og at alle 98 kommuner ville få en pil. Det holder ikke med worst-of. Et fælles forbrugstal på 9,7 ton er højere end de territoriale udledninger i 80 af 98 kommuner, så dimensionen ville stå på præcis samme tal (324 mod en grænse på 3 ton) i de 80 og kun vise en forskel i de 18, hvor de territoriale udledninger er højere. Pilen i de 80 ville være landets, ens for alle. Løsning (b) er stadig den mest ærlige over for, hvad man ved, og den fjerner en skjult indkomstindikator, men prisen er større, end jeg skrev: klimadimensionen holder op med at skelne mellem fire ud af fem kommuner. Derfor er (b) ikke gennemført sammen med trin 1 og afventer en ny stillingtagen. Med det kalibrerede 2011-mønster, som nu er på platformen, afgør de territoriale udledninger dimensionen i 17 kommuner.

### 3.2 Forurening er et gennemsnit uden grænse (E2)

**Fund (beregnet).** Dimensionens fire indikatorer er indbyrdes ukorrelerede (alle korrelationer mellem -0,08 og 0,20), to måles mod en fast grænse (nitrat, genanvendelse) og to mod landsgennemsnittet (pesticider, affald). Gennemsnittet af dem er et tal, hvor 100 ikke svarer til nogen grænse. Det er den eneste dimension, hvor farven hverken kan læses som "inden for grænsen" eller "bedre end landet". Affald og genanvendelse er desuden ikke en planetær grænse, som artikel 2 selv skriver.

**Løsning.** Del dimensionen efter princippet om én grænse pr. dimension:

- *Kemikalier i grundvandet* (nitrat, pesticider og evt. PFAS, se 3.5) med worst-of som de øvrige dimensioner: 18 grønne, 18 gule, 58 røde (94 kommuner med data).
- *Affald og ressourcer* (genanvendelse mod 65 %, affald pr. person): 1 grøn, 7 gule, 90 røde med worst-of.

Det gør ringen til otte dimensioner, og `DoughnutRing` skal tjekkes. Alternativt beholdes dimensionen, men med worst-of inden for hver halvdel og gennemsnit af de to. Den nuværende begrundelse for gennemsnittet, at worst-of ville lade den værste af fire uafhængige kilder bestemme dimensionen, er netop argumentet for, at de fire ikke hører hjemme i samme dimension.

### 3.3 Biodiversitet måler naturværdi mod et mål for beskyttelse

**Fund (vurdering, tal beregnet).** EU's mål om 30 % og 10 % gælder beskyttet og strengt beskyttet areal. Platformen måler andelen af arealet med bioscore mindst 8 og mindst 12, som er DCE's vurdering af arealets værdi for truede arter. Det er to forskellige størrelser: et areal kan være beskyttet med lav bioscore og have høj bioscore uden beskyttelse. Mediankommunen har 4,9 % areal med bioscore mindst 8, og fem kommuner når 30 %. Artikel 2 siger, at målene er politiske, men ikke, at indikatoren måler noget andet end målet.

**Hvad findes (kilde).** Der er ikke kommet en bioscore efter 2021, og Naturkapitalindekset findes kun for 2015 og 2020 og bygger selv på bioscoren. Der findes ingen officiel opgørelse af beskyttet areal pr. kommune. Nationalt indberetter Miljøstyrelsen ca. 15 % beskyttet natur til EU (set via Danmarks Naturfredningsforening, ikke i primærkilden), mens Biodiversitetsrådet (2023) vurderer, at 1,6 % af landarealet reelt kan tælle med, og at intet areal er strengt beskyttet. Trepartsaftalens politiske mål er 20 % beskyttet natur, ikke 30.

**Løsning.** Indikatoren kan blive, men teksten bør sige, at den måler arealets naturværdi og holder den op mod et mål for beskyttelse, og at de to ikke er det samme. En indikator for beskyttet areal pr. kommune kan beregnes af Miljøportalens lag (§3-natur, fredninger, habitat- og fuglebeskyttelsesområder, reservater) efter samme mønster som de øvrige rumlige scripts, men den ville måle beskyttelse på papiret, som Biodiversitetsrådet kritiserer. Jeg ville vente med den, til der findes en officiel opgørelse af, hvad der tæller.

### 3.4 Luftkvalitet kan ikke skelne kommuner

**Fund (beregnet).** PM2.5 ligger mellem 5,6 og 7,5 µg/m³ i alle kommuner. Alle er over WHO's 5, ingen over EU's kommende grænse på 10, og tre over 7,5. NO2 afgør aldrig dimensionen. Dimensionen er rød i alle kommuner, vil være det i mange år, og en kommune kan næppe flytte den, fordi en stor del af partiklerne er langtransporterede. Den siger noget rigtigt om Danmark og næsten intet om forskellen mellem kommuner.

**Løsning.** Behold WHO's retningslinje som loft, og tilføj det, kommunen selv bidrager med. DCE fordeler de nationale emissioner af NOx, PM2.5 og ammoniak på et net på 1 × 1 km (SPREAD-modellen), men data kan ikke hentes åbent; den åbne nordiske udgave slutter i 2014 (kilde). Kommunens egne udledninger til luft kræver derfor en henvendelse til DCE. Indtil da bør dimensionen mærkes som et tilstandsmål, kommunen ikke styrer (3.5).

### 3.5 Tilstand og pres

**Fund (vurdering).** Artikel 2 peger på, at flere indikatorer beskriver det sted, kommunen ligger, mere end det, den gør. Det kan gøres systematisk med miljøindikatorernes standardramme, DPSIR (Smeets & Weterings 1999), som skelner mellem drivkræfter, pres, tilstand, påvirkning og respons. Platformens 15 økologiske indikatorer fordeler sig sådan:

| Type | Indikatorer |
|---|---|
| Pres fra kommunen | territoriale udledninger, forbrugs-CO2 (estimat), affald, grundvandsindvinding, antropiseret areal |
| Tilstand i kommunen | PM2.5, NO2, nitrat, pesticidfund, kvælstofnedfald, vandområdernes tilstand, naturværdi (to) |
| Tilstand i det opland, kommunen er en del af | kvælstof til kystvande |
| Respons | genanvendelse |

Otte af 15 er tilstandsmål, og de ligger i de dimensioner, hvor alle kommuner er røde. En kommune, der handler, kan derfor ikke se det i ringen. Ingen af de to slags er forkerte i en doughnut, men de bør mærkes forskelligt, og de røde tilstandsdimensioner bør have mindst ét pres- eller responsmål ved siden af.

**Løsning.** Et felt `type` (pres, tilstand, respons) i registret, vist som mærke ved indikatoren ligesom "mod mål". Og nye pres- og responsmål, hvor de findes:

- **Arealomlægning (respons, Næringsstoffer og Arealanvendelse).** Statens register over arealomlægningsprojekter, MARS, er åbent som WFS og opdateres dagligt. Hvert projekt har status (forundersøgelse, etableringstilsagn, anlagt), kvælstofeffekt i ton, udtagning og skovrejsning i hektar. Det er den responsindikator, Næringsstoffer mangler: alle 98 kommuner er røde, og kommunens egen indsats kan i dag ikke ses. Registret har intet kommunefelt, så projekterne skal kobles rumligt til kommunegrænserne, og kun ansøgningsrunderne 2025 og 2026 er med. Indsatsbehovet står pr. kystvandopland i samme bilag, som `fetch_kvaelstof_kystvand.py` allerede læser; der findes ingen kommunefordelte kvælstofmål. En indikator kunne være anlagt og tilsagt kvælstofeffekt i procent af indsatsbehovet i de oplande, kommunen afvander til. Den bør vises som kontekst ved siden af scoren, indtil registret har flere år.
- **Kulstofrige lavbundsjorder (pres, Klimapåvirkning eller Arealanvendelse).** Styrelsen for Grøn Arealomlægning og Vandmiljø har en tabel med hektar kulstofrig lavbundsjord for alle 98 kommuner (februar 2025, kun PDF). Det er bruttoareal uanset anvendelse; landbrugsdelen pr. kommune er ikke opgjort, men kan sandsynligvis beregnes ved at krydse Landbrugsstyrelsens tørvelag med markkortet (ikke afprøvet). Det lukker et af de huller, septembernotatet lod stå.
- **PFAS og TFA (tilstand, Forurening).** Begge ligger i den Jupiter-tjeneste, `fetch_grundvand_jupiter.py` allerede bruger. PFAS-4 har status pr. vandværk for ca. 2.030 aktive almene vandværker i 94 kommuner, men næsten ingen prøver efter 2024, formentlig fordi stofkoderne er lagt om; det skal afklares med GEUS, før gruppen bruges. TFA har prøver fra 2025-2026 for ca. 1.980 vandværker i 92 kommuner og er den mest aktuelle kandidat.
- **Kvælstoftilførsel år for år.** DCE opgør tilførslen årligt, men på større kystafsnit end vandområdeplanens oplande, og databasen kræver login. Tallene svinger 40 % med nedbøren, så kun normaliserede tal kan bruges. Jeg fandt ingen åben årlig serie pr. kystvandopland; `naer_kystvand` må fortsat vente på næste vandområdeplan.

## 4. Hvad der holder

Gennemgangen har også kigget efter fejl, der ikke var der. Det bør siges, fordi det er en del af vurderingen.

- Pipelinen er sporbar på et niveau, få tilsvarende platforme når: ét register, ratio beregnet ét sted, et build der nægter at udgive et tal, som ikke kan regnes efter, og en tidsserie der er tvunget til at være samme tal som scoren.
- Den økologiske rings grænsehierarki (biofysisk nedskaleret grænse, så vedtaget mål, så landsgennemsnit) er fagligt velbegrundet og bedre end en ren fordeling pr. indbygger. Kystvandenes målbelastning og grundvandsressourcen pr. kommune er originale bidrag.
- Valget om ikke at lægge kategorierne sammen til ét tal er rigtigt og i tråd med litteraturen.
- Empirisk Bayes for pesticider, treårsværdier for støjende tal og "få tilfælde"-mærket er de rigtige greb. Fund S5 er en udvidelse af dem til resten af ringen, ikke en ny retning.
- De to metodeartikler er usædvanligt åbne om svaghederne. Fundene her kan skrives ind i dem.

## 5. Nye datakilder: samlet oversigt

Status: *bekræftet* betyder, at kilden er åbnet og oplysningen set 15.-16. november 2026. Tabel-id'er hos DST er slået op i Statistikbankens API.

### Sociale ring

| Formål | Kilde | Dækning og år | Adgang | Status og forbehold |
|---|---|---|---|---|
| Aldersstandardisering, sygehus | DST SBR01 | 98 kommuner, 2017-2025, 20 aldersgrupper | Statistikbankens API | Bekræftet og afprøvet i `analyse.py` |
| Aldersstandardisering, hjemmesygepleje | DST HJEMSYG | 98 kommuner, 2016-2025, 8 aldersgrupper | API | Bekræftet og afprøvet. 2025 bygger på første halvår |
| Aldersstandardiseret dødelighed | DST FOD207 | Alle kommuner, etårsalder | API | Bekræftet, ikke afprøvet |
| Kroniske sygdomme, standardiseret | Sundhedsdatastyrelsen, Udvalgte kroniske sygdomme og svære psykiske lidelser | Kommuner, fra 2010, årligt | esundhed.dk | Delvist: dokumentation læst, visningen svarede ikke |
| Alderskorrigeret Sundhedsprofil | danskernessundhed.dk, odds ratio pr. kommune | 98 kommuner, 2025 | Eksport til Excel/CSV | Bekræftet at tallet findes; omregning til andel er mit forslag |
| Stikprøve pr. kommune | Sundhedsprofilen 2025, bilag og svarprocenttabel | 98 kommuner | PDF | Bekræftet |
| Oplevet tryghed | Justitsministeriets Tryghedsundersøgelse 2023 | 98 kommuner, 2023 | PDF | Bekræftet. Ca. 200 svar pr. kommune, ingen nyere udgave fundet |
| Vold og indbrud | DST STRAF11, overtrædelsens art | Alle kommuner, kvartaler til 2026K3 | API | Bekræftet |
| Hjemløshed | VIVE, Hjemløshed i Danmark 2026 | Alle kommuner, hvert andet år | PDF | Bekræftet. Meget små tal |
| Husleje, almene boliger | Landsbyggefonden, Huslejestatistik 2026 | Alle kommuner, årligt | PDF | Bekræftet. Kun almene boliger |
| Bredbånd | DST LABY51 | 98 kommuner, 2014-2025 | API | Bekræftet |
| Kandidater og valgte efter køn | DST LIGEDB2, LIGEDI2 | Alle kommuner, valg 2005-2025 | API | Bekræftet |
| Langtidsledighed, sygedagpenge | DST AULK04, SYGEDP01 | Alle kommuner | API | Bekræftet |
| Ekstern validering | Indenrigs- og Sundhedsministeriet, Kommunerne 2026, tabel 3.2 | Alle kommuner, årligt | PDF | Bekræftet |
| Socioøkonomisk reference for karakterer | Børne- og Undervisningsministeriet | | | Ikke bekræftet pr. kommune |
| Boligbyrde, udsættelser, energimærker, arbejdsulykker, borgertillid | | | | Ikke fundet eller ikke bekræftet pr. kommune |

### Økologiske ring

| Formål | Kilde | Dækning og år | Adgang | Status og forbehold |
|---|---|---|---|---|
| Forbrugsaftryk, nationalt og opdelt | Energistyrelsen, Global Afrapportering 2026, datafil | Landstal 1990-2024 | Excel | Bekræftet. 9,73 ton pr. indbygger i 2024 |
| Forbrugsaftryk pr. kommune efter 2011 | | | | Findes ikke (tre uafhængige kilder) |
| Arealomlægning, fremdrift | MARS, Styrelsen for Grøn Arealomlægning og Vandmiljø | Projekter fra runderne 2025-2026, opdateres dagligt | WFS, lag `mars:projekter_samlet` | Bekræftet. Intet kommunefelt, ingen licens angivet |
| Kulstofrig lavbundsjord | Samme styrelse, opgørelse 7. februar 2025 | 98 kommuner | PDF | Bekræftet. Bruttoareal |
| Tørvelag til egen beregning | Landbrugsstyrelsens WFS, `Toerverig_lavbund_2024` | Landsdækkende | WFS | Laget findes; at det er Kulstof 2022-kortet, er ikke bekræftet |
| PFAS-4 i vandværker | GEUS Jupiter, `jupiter_grp_anlaegsanalyser`, stofgruppe 1104 | 94 kommuner | WFS | Bekræftet, men næsten ingen prøver efter 2024 |
| TFA i vandværker | GEUS Jupiter, `jupiter_anlaegsanalyser`, stofnr. 2251 | 92 kommuner, prøver 2025-2026 | WFS | Bekræftet |
| Egne udledninger til luft | DCE, SPREAD 1 × 1 km | Landsdækkende | Ingen åben download | Kræver henvendelse til DCE |
| Kvælstoftilførsel pr. år | DCE, Vand- og stoftransport; overfladevandsdatabasen | 2. og 3. ordens kystafsnit | Login | Ingen åben serie pr. kystvandopland fundet |
| Beskyttet areal pr. kommune | Miljøportalens WFS (§3, fredninger, Natura 2000) | Landsdækkende lag | WFS | Ingen officiel kommuneopgørelse; kan beregnes |
| HNV-kort | Landbrugsstyrelsens WFS | 2019-2026 | WFS | Bekræftet, ikke vurderet som indikator |
| Ny bioscore, nyt Naturkapitalindeks | | | | Findes ikke |

## 6. Anbefalet rækkefølge

Rækkefølgen følger, hvor meget hvert skridt ændrer det, platformen kan sige, i forhold til prisen.

**Trin 1: rettelser, der ikke rører arkitekturen.** De ændrer offentlige tal og skal i `data/CHANGELOG.md`, men ingen af dem kræver en ny regel.

1. Slå `education` og `low_education` sammen til én indikator med rigtigt navn og gældende mål (S2).
2. Aldersstandardisér `hospital_long`, og tag stilling til `hjemsyg` (S3).
3. Ret nævneren for `vejr_skader` og `music_school` (S4).
4. Kalibrér `forbrug_co2` til Energistyrelsens niveau, og lad grænsen dække samme afgrænsning som tallet (E1, punkt 1 og 2).
5. Skriv de faktiske vægte og DPSIR-typen ind på metodesiden (S1 løsning C, afsnit 3.5).

**Trin 2: usikkerhed.** Treårsgennemsnit for kriminalitet, NEET og fravær, mærket "ikke forskellig fra referencen" og kravet om en tendens bag pilen (S5). Det er det skridt, der gør mest for den faglige troværdighed, fordi det fjerner udsagn, data ikke kan bære. Det kan gennemføres uden at ændre en eneste score.

**Trin 3: beslutninger om metode.** Normaliseringen (S1), absolutte mål i den sociale ring (S6), forbrugsaftrykkets rolle (E1, punkt 3) og opdelingen af Forurening (E2). De hænger sammen og bør tages i én runde, fordi de alle ændrer, hvad en farve betyder. Jeg har givet en anbefaling ved hver, men det er her projektlederens eget bud skal ligge først.

**Trin 4: nye kilder.** Se afsnit 5. Tag dem efter trin 3, så nye indikatorer bygges på den normalisering, der bliver valgt.

Alternativomkostningen ved at begynde med trin 4 er, at nye indikatorer arver de svagheder, trin 1-3 retter. Flere indikatorer gør ikke ringen stærkere, så længe vægtene inden for en kategori er tilfældige, og usikkerheden ikke vises.

## 7. Hvad gennemgangen ikke dækker

- **Ingen ny kode i pipelinen.** Løsningerne er afprøvet i `analyse.py` på de committede data, ikke bygget ind i fetch-scripterne. Tallene for standardisering og nævnere viser størrelsesordenen; de endelige tal kan afvige lidt, når de regnes i pipelinen med dens egne årgange.
- **Støjmålet er en model.** Spredningen om en lineær udvikling over otte år antager, at den sande udvikling er jævn. Et reelt knæk (en skolelukning, en ny motorvej) tælles som støj. Indikatorer, der allerede er treårsgennemsnit, får for lav støj, fordi årene overlapper. Tallene for hvor mange farver der er usikre, er derfor størrelsesordener.
- **Sundhedsprofilens otte indikatorer er ikke aldersstandardiseret her,** og deres usikkerhed er et skøn ud fra en antaget stikprøve på 900 svar, ikke regnet på hver kommunes faktiske antal.
- **Ekstern validering mangler.** Den sociale ring er ikke holdt op mod et uafhængigt mål, fx Indenrigsministeriets socioøkonomiske indeks. Det ville vise, om ringen fanger mere end den ene socioøkonomiske linje, artikel 1 finder.
- **Ingen brugertest.** Om en bruger læser "ikke forskellig fra referencen" eller en standardiseret skala rigtigt, er ikke undersøgt. Artikel 1 nævner samme hul.
- **Retningspilenes regler i øvrigt** (medianen som skel mellem rigtig og tempo, endepunkternes gennemsnit) er ikke gennemgået ud over signifikanstesten.
- **Webappens kode og formidling** er ikke gennemgået.

## 8. Referencer

Bibliografiske oplysninger er kontrolleret mod DOI-opslag eller udgiverens side 15.-16. november 2026, medmindre andet står.

- Ahmad, O.B., Boschi-Pinto, C., Lopez, A.D., Murray, C.J.L., Lozano, R. & Inoue, M. (2001). Age standardization of rates: a new WHO standard. GPE Discussion Paper Series No. 31. World Health Organization.
- Akenji, L., Bengtsson, M., Toivio, V., Lettenmeier, M., Fawcett, T., Parag, Y., Saheb, Y., Coote, A., Spangenberg, J.H., Capstick, S., Gore, T., Coscieme, L., Wackernagel, M. & Kenner, D. (2021). 1.5-Degree Lifestyles: Towards A Fair Consumption Space for All. Berlin: Hot or Cool Institute. (Registret og metodesiden citerer rapporten som "Hot or Cool Institute 2021".)
- Becker, W., Saisana, M., Paruolo, P. & Vandecasteele, I. (2017). Weights and importance in composite indicators: Closing the gap. Ecological Indicators, 80, 12-22. doi:10.1016/j.ecolind.2017.03.056
- Danmarks Statistik. Dokumentation af variablen ERHAUDD (erhvervskompetencegivende uddannelser er DISCED-hovedgrupperne 30-80). https://www.dst.dk/da/Statistik/dokumentation/Times/Uddannelsesdata/Hoejest-fuldfoerte-uddannelse---status/ERHAUDD
- Fanning, A.L. & Raworth, K. (2025). Doughnut of social and planetary boundaries monitors a world out of balance. Nature, 646, 47-56. doi:10.1038/s41586-025-09385-1
- Goldstein, H. & Spiegelhalter, D.J. (1996). League tables and their limitations: statistical issues in comparisons of institutional performance. Journal of the Royal Statistical Society: Series A, 159(3), 385-443. doi:10.2307/2983325
- Mann, H.B. (1945). Nonparametric tests against trend. Econometrica, 13(3), 245-259. doi:10.2307/1907187
- Mazziotta, M. & Pareto, A. (2016). On a generalized non-compensatory composite index for measuring socio-economic phenomena. Social Indicators Research, 127(3), 983-1003. doi:10.1007/s11205-015-0998-2. (Bibliografien er kontrolleret; at skalaen er 100 med standardafvigelse 10, er efter min hukommelse og ikke kontrolleret i teksten.)
- McLennan, D., Noble, S., Noble, M., Plunkett, E., Wright, G. & Gutacker, N. (2019). The English Indices of Deprivation 2019: Technical report. London: Ministry of Housing, Communities and Local Government.
- OECD, European Union & Joint Research Centre (2008). Handbook on Constructing Composite Indicators: Methodology and User Guide. Paris: OECD Publishing. doi:10.1787/9789264043466-en. (Bibliografien er kontrolleret; indholdet er gengivet efter min hukommelse.)
- O'Neill, D.W., Fanning, A.L., Lamb, W.F. & Steinberger, J.K. (2018). A good life for all within planetary boundaries. Nature Sustainability, 1(2), 88-95. doi:10.1038/s41893-018-0021-4
- Paruolo, P., Saisana, M. & Saltelli, A. (2013). Ratings and rankings: voodoo or science? Journal of the Royal Statistical Society: Series A, 176(3), 609-634. doi:10.1111/j.1467-985X.2012.01059.x
- Regeringen m.fl. (2006). Aftale om udmøntning af globaliseringspuljen, 2. november 2006. https://bm.dk/media/6549/globaliseringspuljen_samlet_aftale2006.pdf
- Rigsrevisionen (2012). Beretning til Statsrevisorerne om indsatsen for at få flere unge til at gennemføre en ungdomsuddannelse. Beretning 10/2011. https://rigsrevisionen.dk/Media/1/F/10-2011.pdf
- Rigsrevisionen (2019). Notat til Statsrevisorerne, august 2019 (om afløsningen af 95 %-målsætningen). https://rigsrevisionen.dk/Media/6/5/1406-19.pdf
- Smeets, E. & Weterings, R. (1999). Environmental indicators: Typology and overview. Technical report No 25. København: European Environment Agency.
- Spiegelhalter, D.J. (2005). Funnel plots for comparing institutional performance. Statistics in Medicine, 24(8), 1185-1202. doi:10.1002/sim.1970

Øvrige kilder (Osei-Owusu m.fl. 2020, Energistyrelsen 2026, Richardson m.fl. 2023 m.fl.) står i `docs/oekologisk-gennemgang-sep-2026.md` og i de to metodeartikler.

### Kilder til mål og data

Mål:

- Aftale om bedre veje til uddannelse og job (2017), gengivet af KL: https://www.kk.dk/sites/default/files/agenda/9036be1a-2df7-4c99-b05d-d5dc932425d2/6196140d-263a-4b68-9ca4-b428222c7187-bilag-3.pdf og Reformkommissionen: https://reformkommissionen.dk/media/oxqcnxbb/faktaark_unge-uden-uddannelse_a.pdf
- Finansministeriet (2025). Denmark's Annual Progress Report 2025, appendiks C (nationale 2030-mål). https://en.fm.dk/media/ijsj5ysn/denmark-s-annual-progress-report-2025-a.pdf
- Det Nationale Partnerskab mod Ensomhed (2023). Sammen mod ensomhed - en national 2040 strategi. https://www.rodekors.dk/sites/rodekors.dk/files/2023-09/National%20ensomhedsstrategi%202023-WEB.pdf
- Røgfri Fremtid. https://www.cancer.dk/roegfri-fremtid/om-roegfri-fremtid
- Færdselssikkerhedskommissionen. Handlingsplan 2021-2030, resumé. https://www.faxekommune.dk/sites/default/files/bilag/faerdselssikkerhedskommissionens_nationale_handlingsplan_resume_2021-2030.pdf
- Danmarks Statistik (2018). Fattigdomsindikatorer er ikke en ny fattigdomsgrænse. https://www.dst.dk/da/presse/Pressemeddelelser/2018/2018-07-16-fattigdomsindikatorer-er-ikke-en-ny-fattigdomsgraense

Sociale data:

- Den Nationale Sundhedsprofil, vejledning og baggrund: https://www.danskernessundhed.dk/Vejledning.html, https://www.danskernessundhed.dk/Baggrund.html. Rapport 2025: https://www.sdu.dk/sif/-/media/images/sif/udgivelser/2026/den_nationale_sundhedsprofil_2025.pdf
- Sundhedsdatastyrelsen, informationsfane for Udvalgte kroniske sygdomme og svære psykiske lidelser: https://cdn1.gopublic.dk/sundhedsdatastyrelsen/Media/638941202140187084/Informationsfane%20for%20statistikken%20Udvalgte%20Kroniske%20Sygdomme%20og%20Sv%C3%A6re%20Psykiske%20Lidelser.pdf
- Justitsministeriet (2024). Tryghedsundersøgelsen 2023. https://www.justitsministeriet.dk/wp-content/uploads/2024/04/tryghedsundersoegelse-2023.pdf
- VIVE (2026). Hjemløshed i Danmark 2026. https://www.vive.dk/media/pure/4z6bg0ov/31475673
- Landsbyggefonden (2026). Huslejestatistik 2026. https://www.lbf.dk/media/fplnqrwm/huslejestatistik-2026.pdf
- Indenrigs- og Sundhedsministeriet (2026). Kommunerne 2026. https://www.ism.dk/Media/639039931769753840/Kommunerne_2026.pdf
- DST-tabeller: https://api.statbank.dk/v1/tableinfo/<tabel-id>

Økologiske data:

- Energistyrelsen (2026). Global Afrapportering 2026, datafil. https://ens.dk/media/8503/download
- Klimarådet (2023). Baggrundsnotat 2: Danmarks forbrugsbaserede klimaaftryk. https://klimaraadet.dk/sites/default/files/node/field_files/Baggrundsnotat%202%20-%20Danmarks%20forbrugsbaserede%20klimaaftryk.pdf
- Hot or Cool Institute (2025). A Climate for Sufficiency. https://hotorcool.org/wp-content/uploads/2025/10/A_Climate_for_Sufficiency_report_FULL_REPORT-1.pdf
- Sanderson, H. m.fl. (2024). Frontiers in Climate. https://www.frontiersin.org/journals/climate/articles/10.3389/fclim.2023.1294296/full (kun citatet om manglende kommunale opgørelser er brugt; øvrige bibliografiske oplysninger er ikke kontrolleret)
- Jack, T. & Ivanova, D. (2021). Energy Research & Social Science, 78, 102130. https://eprints.whiterose.ac.uk/id/eprint/174442/17/1-s2.0-S2214629621002231-main.pdf (titel ikke kontrolleret)
- NIRAS (2024). Rapport om forbrugsbaserede klimaaftryk på lokalt niveau. https://www.kl.dk/media/wqhov21i/niras-rapport-om-forbrugsbaserede-klimaaftryk-paa-lokalt-niveau.pdf
- MARS, WFS: https://mars.sgav.dk/geo/wfs?service=WFS&version=1.0.0&request=GetCapabilities. Om registret: https://www.sgav.dk/groen-trepart/lokale-treparter/mars
- Styrelsen for Grøn Arealomlægning og Vandmiljø (2025). Opgørelse af kulstofrige lavbundsjorder fordelt på deloplande, kommuner og lokale treparter. https://www.sgav.dk/Media/638745209891164350/Opg%C3%B8relse%20af%20kulstofrige%20lavbundsjorder%20fordelt%20p%C3%A5%20deloplande,%20kommuner%20og%20lokale%20treparter.pdf
- GEUS Jupiter, WFS: https://data.geus.dk/geusmap/ows/25832.jsp
- Landbrugsstyrelsen, WFS: https://geodata.fvm.dk/geoserver/wfs
- DCE, geografisk fordeling af emissioner (SPREAD): https://envs.au.dk/en/research-areas/air-pollution-emissions-and-effects/air-emissions/spatial-distribution
- DCE (2024). Vand- og stoftransport 2023. Videnskabelig rapport nr. 629. https://dce.au.dk/fileadmin/dce.au.dk/Udgivelser/Videnskabelige_rapporter_600-699/SR629.pdf
- Biodiversitetsrådet (2023). Årsrapport 2023. https://www.biodiversitetsraadet.dk/viden/aarsrapport-2023
- Naturkapitalindekset: https://biodiversitet.nu/naturkapital
