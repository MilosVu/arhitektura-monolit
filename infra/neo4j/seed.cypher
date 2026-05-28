MERGE (l:Law {ref: 'stgb-146'})
SET l.title = 'Schweizerisches Strafgesetzbuch',
    l.article = 'Art. 146 Betrug',
    l.content = 'Wer in der Absicht, sich oder einen Dritten unrechtmässig zu bereichern, durch Täuschung oder arglistige Täuschung des Irrtums eines andern fremdes Vermögen schädigt, wird mit Freiheitsstrafe bis zu fünf Jahren oder Geldstrafe bestraft.',
    l.valid_from = date('2020-01-01');

MERGE (l:Law {ref: 'or-41'})
SET l.title = 'Obligationenrecht',
    l.article = 'Art. 41 Schadenersatz',
    l.content = 'Wer unrichtig, unsorgfältig oder in Übertretung vertraglicher oder gesetzlicher Pflichten einen Schaden verursacht, haftet dem Geschädigten für dessen Behebung.',
    l.valid_from = date('2020-01-01');

MERGE (l:Law {ref: 'zpo-80'})
SET l.title = 'Zivilprozessordnung',
    l.article = 'Art. 80 Beweis',
    l.content = 'Das Gericht würdigt die Beweise nach der freien Überzeugung. Es darf Beweismittel nur berücksichtigen, die rechtsgültig erhoben worden sind.',
    l.valid_from = date('2020-01-01');
