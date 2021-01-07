while IFS= read -r line; do
  if [line != ${line,,}] 
  then
  	echo "$line" >> "words2.txt"
  fi
done < "words.txt"