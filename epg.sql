CREATE TABLE channel (
  ch_id VARCHAR(10) PRIMARY KEY,
  disp_name VARCHAR(80) UNIQUE NOT NULL,
  disp_name_l VARCHAR(80) UNIQUE NOT NULL,
  icon VARCHAR(80)
);

CREATE TABLE programme (
  channel VARCHAR(10) NOT NULL,
  pstart TIMESTAMP(0) NOT NULL,
  pstop TIMESTAMP(0) NOT NULL,
  title VARCHAR(400),
  pdesc VARCHAR(1500),
  cat VARCHAR(50),
  constraint channel_fk FOREIGN KEY (channel) REFERENCES channel(ch_id)
);
