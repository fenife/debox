package config

import (
	"encoding/json"
	"fmt"
	"os"
)

type ServerConfig struct {
	Host string `json:"host"`
	Port int    `json:"port"`
}

func (s *ServerConfig) ServerAddr() string {
	return fmt.Sprintf("%s:%d", s.Host, s.Port)
}

type MysqlConfig struct {
	Host     string `json:"host"`
	Port     int    `json:"port"`
	User     string `json:"user"`
	Password string `json:"password"`
	Database string `json:"database"`
	Charset  string `json:"charset"`
}

func (c *MysqlConfig) ConnStr() string {
	// https://gorm.io/docs/connecting_to_the_database.html#MySQL
	return fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		c.User, c.Password, c.Host, c.Port, c.Database,
	)
}

type RedisConfig struct {
	Host string `json:"host"`
	Port int    `json:"port"`
}

func (r *RedisConfig) Addr() string {
	return fmt.Sprintf("%s:%d", r.Host, r.Port)
}

type AdminUser struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type Config struct {
	Env    string       `json:"env"`
	Server ServerConfig `json:"server"`
	Mysql  MysqlConfig  `json:"mysql"`
	Redis  RedisConfig  `json:"redis"`
}

var Conf Config

func init() {
	// 相对 main.go 执行文件的路径，在项目根目录下
	configFile := "./config.json"
	data, err := os.ReadFile(configFile)
	if err != nil {
		panic(fmt.Sprintf("read config file failed: %v", err))
	}
	if err := json.Unmarshal(data, &Conf); err != nil {
		panic(fmt.Sprintf("unmarshal config data failed: %v", err))
	}
}
