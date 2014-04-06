Speakers: Johan Martinsson
Title: Refactorer legacy, même pas peur !
Slug: refactorer-legacy-meme-pas-peur
Date: 2014-04-06 12:11
Subtitle: Disposer rapidement d’une couverture de code sur du legacy pour le refactorer, mission impossible ? Venez apprendre ce tour de magie!
Goal: Mieux armés pour écrire des tests destintés au refactoring
Duration: 50 minutes
Format: Conférence participative
Tags: Construire
Summary: Le code legacy est souvent synonyme de difficilement lisible et évolutif. Refactorer le code reste trop dangereux sans disposer de tests. Néanmoins, les écrire préalablement est souvent perçu comme TRÈS long et n’est donc pas fait. Est-ce possible à la fois d’écrire très rapidement des tests qui ont une couverture de code proche de 100% et qui ne sont pas fragiles au remaniement du code et du design ? OUI, en utilisant l'approche Golden Master.


L’idée est d’écrire des tests temporaires spécifiques à l’activité de refactoring qui bombardent la partie du code à remanier en faisant varier les arguments en entrée et compare la sortie avec une référence qui a été enregistré avec le code initial. Le tour de force est d’automatiser tout cela grâce un outillage adapté comme Approvals Test. Après le refactoring, des tests classiques remplaceront ces tests temporaires.

Venez vous entraîner sur cette pratique sur des cas concrets tirés de notre expérience sur divers projets réels avec des dépendences externes (web services tiers, fichiers…) et des effets de bords.

Notre session sera une réussite si vous utiliserez cette pratique dès le lendemain sur vos projets.


