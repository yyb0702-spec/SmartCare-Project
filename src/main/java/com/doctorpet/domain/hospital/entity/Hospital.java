package com.doctorpet.domain.hospital.entity;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Getter
@Entity
@Table(name = "hospitals")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Hospital {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "mgmt_no",nullable = false, unique = true)
    private String mgmtNo;

    @Column(name = "local_gov_code")
    private String localGovCode;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String phone;

    @Column(name = "address_jibun", nullable = false)
    private String addressJibun;

    @Column(name = "address_road", nullable = false)
    private String addressRoad;

    private String zipcode;

    @Column(name = "cord_x", nullable = false, precision = 15, scale = 10)
    private BigDecimal cordX;

    @Column(name = "cord_y", nullable = false, precision = 15, scale = 10)
    private BigDecimal cordY;

    @Column(name = "license_date", nullable = false)
    private LocalDate licenseDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "business_status", nullable = false)
    private BusinessStatus businessStatus;

    @Column(name = "close_date")
    private LocalDate closeDate;

    @Column(precision = 12, scale = 2)
    private BigDecimal area;

    @Column(name = "source_modified_at")
    private LocalDateTime sourceModifiedAt;

    @Enumerated(EnumType.STRING)
    @Column(name = "partnership_status", nullable = false)
    private PartnershipStatus partnershipStatus;

    private Hospital(
            String mgmtNo,
            String localGovCode,
            String name,
            String phone,
            String addressJibun,
            String addressRoad,
            String zipcode,
            BigDecimal cordX,
            BigDecimal cordY,
            LocalDate licenseDate,
            BusinessStatus businessStatus,
            LocalDate closeDate,
            BigDecimal area,
            PartnershipStatus partnershipStatus
    ) {
        this.mgmtNo = mgmtNo;
        this.localGovCode = localGovCode;
        this.name = name;
        this.phone = phone;
        this.addressJibun = addressJibun;
        this.addressRoad = addressRoad;
        this.zipcode = zipcode;
        this.cordX = cordX;
        this.cordY = cordY;
        this.licenseDate = licenseDate;
        this.businessStatus = businessStatus;
        this.closeDate = closeDate;
        this.area = area;
        this.partnershipStatus = partnershipStatus;
    }

    public static Hospital create(
            String mgmtNo,
            String localGovCode,
            String name,
            String phone,
            String addressJibun,
            String addressRoad,
            String zipcode,
            BigDecimal cordX,
            BigDecimal cordY,
            LocalDate licenseDate,
            BusinessStatus businessStatus,
            LocalDate closeDate,
            BigDecimal area,
            PartnershipStatus partnershipStatus
    ) {
        return new Hospital(
                mgmtNo,
                localGovCode,
                name,
                phone,
                addressJibun,
                addressRoad,
                zipcode,
                cordX,
                cordY,
                licenseDate,
                businessStatus,
                closeDate,
                area,
                partnershipStatus
        );
    }

    // 공공 데이터 최종 업데이트 날짜 기록
    public void updateSourceModifiedAt(LocalDateTime sourceModifiedAt) {
        this.sourceModifiedAt = sourceModifiedAt;
    }

}
