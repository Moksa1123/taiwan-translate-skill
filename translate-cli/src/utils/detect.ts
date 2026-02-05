import * as fs from 'fs';
import * as path from 'path';
import type { AIType } from '../types/index.js';
import { AI_FOLDERS, AI_DISPLAY_NAMES } from '../types/index.js';

interface DetectionResult {
  detected: AIType[];
  suggested: AIType | null;
}

/**
 * 偵測當前目錄中存在哪些 AI 平台的資料夾
 */
export function detectAIType(): DetectionResult {
  const cwd = process.cwd();
  const detected: AIType[] = [];

  for (const [aiType, folders] of Object.entries(AI_FOLDERS)) {
    for (const folder of folders) {
      const folderPath = path.join(cwd, folder);
      if (fs.existsSync(folderPath)) {
        detected.push(aiType as AIType);
        break;
      }
    }
  }

  // 建議第一個偵測到的平台，如果都沒有則預設 claude
  const suggested = detected.length > 0 ? detected[0] : 'claude' as AIType;

  return { detected, suggested };
}

/**
 * 取得 AI 平台的顯示名稱
 */
export function getAITypeDescription(aiType: AIType | string): string {
  if (aiType === 'all') return '全部安裝';
  return AI_DISPLAY_NAMES[aiType as Exclude<AIType, 'all'>] || aiType;
}

/**
 * 檢查是否為有效的 AI 類型
 */
export function isValidAIType(aiType: string): aiType is AIType {
  return aiType === 'all' || aiType in AI_FOLDERS;
}

/**
 * 取得平台的資料夾路徑
 */
export function getAIFolder(aiType: Exclude<AIType, 'all'>): string {
  return AI_FOLDERS[aiType][0];
}
