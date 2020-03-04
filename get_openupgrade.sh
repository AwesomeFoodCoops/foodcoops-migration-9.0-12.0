#!/bin/bash
cd /
mkdir openupgrade
cd openupgrade
mkdir -p 9.0 10.0 11.0 12.0

# make checkouts if they do not exist
for branch in $(ls -v -d */ | sed 's@/@@'); do
  echo 'downloading branch: '$branch
  if ! [ -d $branch/.git ]; then
    (rmdir $branch &&
      git clone https://github.com/OCA/OpenUpgrade.git -b $branch $branch --single-branch --depth 1)
  else
    (cd $branch && git fetch && git reset --hard origin/$branch)
  fi
done
