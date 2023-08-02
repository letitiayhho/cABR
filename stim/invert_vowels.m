cd /Users/letitiaho/src/cabr/stim

files = dir('*.wav');
for i = 1:length(files)
    file = files(i).name;
    
    % Read audio
    fprintf(1, ['Reading ', file, '\n'])
    [y, Fs] = audioread(file);
    
    % Invert audio
    y_inverted = y*-1;

    % Split up the original filename to create new filename
    parts = split(file, '.');
    stem = char(parts(1));
    suffix = char(parts(2));
    newfile = [stem, '_inverted.', suffix];
    
    % Save inverted .wav file
    fprintf(1, ['Writing ', newfile, '\n'])
    audiowrite(newfile, y_inverted, Fs);
end