export const captureScreenshot = async (): Promise<string> => {
  try {
    const canvas = await chrome.tabs.captureVisibleTab();
    return canvas;
  } catch (error) {
    console.error('Screenshot capture error:', error);
    throw new Error('Failed to capture screenshot');
  }
};

export const extractPriceData = (
  screenshot: string,
): Promise<{
  closes: number[];
  highs: number[];
  lows: number[];
  volumes: number[];
} | null> => {
  // NOTE: This is placeholder - actual implementation requires
  // OCR/image processing to extract candle data from chart
  // For Phase 1, use mock data or require manual entry

  return Promise.resolve({
    closes: [64000, 64100, 64050, 64150, 64200],
    highs: [64100, 64150, 64150, 64250, 64300],
    lows: [63950, 64000, 64000, 64100, 64150],
    volumes: [1000, 1200, 900, 1100, 1300],
  });
};
