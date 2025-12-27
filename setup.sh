#This is just a basic shell script to check if all required modules are installed.
echo "Checking if packages are installed..."
for pkg in "git" "python3"; do
	cmd=$( which $pkg )
	if [[ $cmd == "" ]]; then
		echo $pkg "is not installed."
		echo "Installing "$pkg"..."
		sudo apt install $pkg
		
	else
		echo $pkg "is installed."
	fi
done	
echo "Running Python setup script..."
python3 setup.py

