flake8 src
if [ $? -eq 0 ]
then
    echo "code formatted well"
else
    echo "PLZ format your code"
fi
