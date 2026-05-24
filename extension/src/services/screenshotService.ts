/**
 * Screenshot Capture Service
 * Handles capturing visible tabs and extracting chart data
 */

interface PriceData {
  closes: number[];
  highs: number[];
  lows: number[];
  volumes: number[];
}

/**
 * Capture the current visible tab as a data URL string
 */
export const captureScreenshot = async (): Promise<string> => {
  try {
    if (!chrome.tabs) {
      throw new Error("Chrome tabs API not available");
    }

    const canvas = await chrome.tabs.captureVisibleTab();
    if (!canvas) {
      throw new Error("Failed to capture screenshot");
    }
    return canvas;
  } catch (error) {
    console.error("Screenshot capture error:", error);
    throw new Error(
      `Failed to capture screenshot: ${error instanceof Error ? error.message : String(error)}`
    );
  }
};

/**
 * Extract price data from a chart screenshot
 * NOTE: This is a placeholder - actual implementation requires:
 * - OCR (Tesseract.js or similar) to read price labels
 * - Image processing (canvas API) to detect candle patterns
 * - AI vision (GPT-4V) for intelligent chart analysis
 * 
 * For now, returns mock data or requires manual entry in UI
 */
export const extractPriceData = async (
  _screenshot: string
): Promise<PriceData | null> => {
  try {
    // Placeholder: Return mock data
    // In production, integrate with image processing library
    return {
      closes: [64000, 64100, 64050, 64150, 64200],
      highs: [64100, 64150, 64150, 64250, 64300],
      lows: [63950, 64000, 64000, 64100, 64150],
      volumes: [1000, 1200, 900, 1100, 1300],
    };
  } catch (error) {
    console.error("Price data extraction error:", error);
    return null;
  }
};

/**
 * Convert image to base64 string for API transmission
 */
// eslint-disable-next-line no-unreachable
export const imageToBase64 = async (
  imageUrl: string
): Promise<string> => {
  const response = await fetch(imageUrl);
  if (!response.ok) {
    throw new Error(`Failed to fetch image: ${response.statusText}`);
  }

  const blob = await response.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64 = reader.result as string;
      resolve(base64);
    };
    reader.onerror = () => {
      reject(new Error("Failed to read file"));
    };
    reader.readAsDataURL(blob);
  });
};
