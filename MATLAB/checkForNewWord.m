% checkForNewWord
% reads to look for a new word.
% returns a string

function newWord = checkForNewWord(conn)
% newWord = ''
newWord = fscanf(conn, '%s');
if strcmp(newWord, '')
    newWord = '';
else
    newWord = extractBefore(newWord, '~');
end
flushinput(conn);
% if you don't want to add a new word, leave as ''
end