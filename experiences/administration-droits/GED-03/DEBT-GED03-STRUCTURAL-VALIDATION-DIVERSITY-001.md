# DEBT-GED03-STRUCTURAL-VALIDATION-DIVERSITY-001

Status: OPEN — non-blocking for phase 1
Profile: ULISDOQ-PROFILE-EML-GENERIC-CANDIDATE

## Observation

The bounded synthetic corpus passed 9/9. This does not qualify generic real-world EML structural validation.

## Debt

Before qualification, broaden independent tests around unusual but valid RFC/MIME messages, nested message/rfc822, optional/missing headers, charset and transfer-encoding defects, duplicate headers, multipart nesting and parser defects not represented in GED-03 phase 1.

The current distinction between MALFORMED and TRUNCATED uses parser defects plus profile-required header completeness. It is a phase-1 candidate rule, not a universal RFC validity rule.

## Phase-1 decision

NON_BLOCKING=YES
PROFILE_QUALIFICATION=NONE
PRODUCTION_QUALIFICATION=NO
GED03_PHASE1_CAN_ADVANCE=YES