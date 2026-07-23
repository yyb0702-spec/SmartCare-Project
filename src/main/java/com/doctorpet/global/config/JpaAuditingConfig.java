package com.doctorpet.global.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/** BaseEntity의 createdAt/updatedAt 자동 기록을 활성화한다. */
@Configuration
@EnableJpaAuditing
public class JpaAuditingConfig {
}
