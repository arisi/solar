echo cloning and installing stuff... takes few minutes...
sudo apt-get install build-essential zlib1g-dev libssl-dev libreadline-dev git-core curl libyaml-dev ruby-dev nodejs -y
sudo gem install bundle
git clone https://github.com/arisi/rsinatra.git
cd rsinatra
bundle
./rsinatra.rb