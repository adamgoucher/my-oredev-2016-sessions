# Jenkins Pipeline

*Heuristic* - Don't use AWS CodeDeploy the way AWS says to use it with Jenkins -- they want you to recompile and repackage on every deployment

My delivery pipeline
* 01-contests-build-and-package
* 05-contests-deploy-to-humans
* 10-contests-deploy-to-production
* 15-contests-deploy-to-sales

01-contests-build-and-package is the workhorse
- fetches code
- writes the build number to the .env.* files which is displayed in all our footer (Note: will break if .env.* files are not checked in with a newline at the end of them.)
```shell
set +e

for FILE in .env*
do
  if grep -q "VERSION=" ${FILE}
  then
    sed -i "s/^VERSION=.*/VERSION=${BUILD_TIMESTAMP}/" ${FILE}
  else
    echo "VERSION=${BUILD_TIMESTAMP}" >> ${FILE}
  fi
done
```
- composer (including dev, and fails build when any Warnings or Errors) 
```shell
composer clearcache

rm -f storage/logs/composer.log
composer install --verbose --optimize-autoloader 2>&1 | tee storage/logs/composer.log

if grep -c "Problem" storage/logs/composer.log
then
  exit 1
fi

if grep -c "Warning" storage/logs/composer.log
then
  exit 2
fi
```
- PSR2 checks
- phpunit (with code coverage every 15 builds)
```shell
mkdir -p jenkins/phpunit
mkdir -p jenkins/phpunit/clover

# run coverage only every 15 builds
if [ $(($BUILD_ID%15)) -eq 0 ]; then
  ./vendor/bin/phpunit --log-junit jenkins/phpunit/junit.xml --coverage-clover jenkins/phpunit/clover.xml --coverage-html jenkins/phpunit/clover
else
  ./vendor/bin/phpunit --log-junit jenkins/phpunit/junit.xml
fi
```
- remove the dev packages from composer
- zip the whole thing up and put in an S3 bucket for CodeDeploy
```shell
zip -r ${BUILD_TIMESTAMP}.zip . -x *.git* **/*.log storage/framework/views/* jenkins/**\* tests/**\* storage/framework/views/* storage/app/database/*
aws s3 cp ${BUILD_TIMESTAMP}.zip s3://mxco-releases/contests/
echo "revision=${BUILD_TIMESTAMP}" > codedeploy.properties
rm ${BUILD_TIMESTAMP}.zip
```
- store codeploy.properties as an artifact of the build

05-contests-deploy-to-humans then reads codedeploy.properties from 01-contests-build-and-deploy as input to
- create a deployment
```shell
if [ -f codedeploy.id ]; then
  rm codedeploy.id
fi
aws deploy create-deployment \
--application-name contests \
--deployment-group-name humans \
--s3-location bucket=mxco-releases,bundleType=zip,key=contests\/$revision.zip \
--output text \
--region us-west-2 > codedeploy.id
```
- deploy the revision
```shell
aws deploy get-deployment \
--region us-west-2 \
--deployment-id `cat codedeploy.id` > codedeploy.status

while (grep -q "\"status\": \"Created\"," codedeploy.status || grep -q "\"status\": \"InProgress\"," codedeploy.status)
do
  sleep 10
  aws deploy get-deployment \
  --region us-west-2 \
  --deployment-id `cat codedeploy.id` > codedeploy.status
done

if grep -q "\"status\": \"Failed\"," codedeploy.status
then
  exit 1
elif grep -q "\"status\": \"Succeeded\"," codedeploy.status
then  
  exit 0
else
  exit 2
fi
```

The other jobs then read from 05-contests-deploy-to-humans as that is our testing environment. With some Role Based permissions inside Jenkins we can control exactly what goes into which environment, by whom and can see what is there currently.

Note: Since this was constructed, AWS CodeBuild has been released. If I was to do it again, I would just use it.
