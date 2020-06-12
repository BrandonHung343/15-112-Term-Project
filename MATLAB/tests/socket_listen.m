% opens a socket and reads for it 10 times
conn = tcpip('127.0.0.1', 4000);
conn.InputBufferSize = 1024;
count = 0;
conn.Timeout = 30;
conn.Terminator = '0';
fopen(conn);

while count < 10
    newWord = checkForNewWord(conn);
    if strcmp(newWord, 'exit')
        break
    end
    count = count + 1;
    disp(count)
end
fclose(conn);
delete(conn);
clear conn

