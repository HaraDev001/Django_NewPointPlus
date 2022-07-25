# バッチ処理用のコマンド
aws s3 cp s3://${NewPointPlusConfigBucket}/${EnvFileS3Directory}/.env.${Env} ./.env --region ${Region} &&
python manage.py ${COMMAND} ${PARAMETER}

exit $?
