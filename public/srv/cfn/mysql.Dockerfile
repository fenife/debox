
FROM mysql:5.7.30

COPY my.cnf /etc/mysql/conf.d/

CMD ["mysqld"]

ENTRYPOINT ["docker-entrypoint.sh"]


