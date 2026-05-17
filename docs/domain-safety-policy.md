# Domain Safety Policy

## Purpose

법령·고시·감정평가 관련 응답은 참고용 검토 보조다. 시스템은 근거와 source metadata를 정리할 수 있지만 최종 법률 판단, 적법성 판단, 감정평가 적정성 판단을 단정하지 않는다.

## Required Copy

Reusable notice:

> 이 응답은 참고용 검토 보조이며 최종 법률 또는 전문 판단이 아닙니다. 법령·고시·감정평가 관련 결론은 원문과 전문가 검토로 확인하세요.

When data is not official:

> sample/user_provided/unknown 자료는 official data로 간주하지 마세요.

When evidence is insufficient:

> 근거 부족 상태이므로 출처 확인 및 추가 자료가 필요합니다.

When official metadata is missing:

> 출처 확인 필요: `[field]` metadata가 부족합니다. 부족한 공식 metadata는 임의로 보완하지 않습니다.

## Prohibited Copy

Do not say:

- 위법입니다
- 적법합니다
- 법적 책임이 있습니다
- 감정평가가 부적정합니다
- 확정 판정

## Manual Supplementation

Manual supplementation may fill verifiable metadata from official source pages or documents. It must not fill conclusions, legal liability, or appraisal appropriateness.

## Agent Limitation

The agent cannot certify legal/professional conclusions. It can preserve metadata, show evidence limits, and point to source verification needs.

## Prerequisite Work

- Better official source coverage
- Human review workflow
- UI/API surfaces for missing metadata and insufficient evidence state
- Legal/professional review policy if production users rely on outputs
