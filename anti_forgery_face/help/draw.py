import cv2

def plot(img, bbox = [], text = "", color_line = (0, 255, 128), color_text = (64, 64, 255), thickness = 1):
            thickness_virtual = thickness*2
            # print("bbox:",bbox)
            box =bbox
        # for box in bbox:
            x, y, x1, y1 = box[0], box[1], box[2], box[3]
            lx = int ((x1 - x)*0.2)
            ly = int ((y1 - y)*0.2)
            
            cv2.rectangle(img, (x,y), (x1, y1), color_line, thickness)
            # Top Left  x,y
            cv2.line(img, (x, y), (x + lx, y), color_line, thickness_virtual)
            cv2.line(img, (x, y), (x, y + ly), color_line, thickness_virtual)
            # Top Right  x1,y
            cv2.line(img, (x1, y), (x1 - lx, y), color_line, thickness_virtual)
            cv2.line(img, (x1, y), (x1, y + ly), color_line, thickness_virtual)
            # Bottom Left  x,y1
            cv2.line(img, (x, y1), (x + lx, y1), color_line, thickness_virtual)
            cv2.line(img, (x, y1), (x, y1 - ly), color_line, thickness_virtual)
            # Bottom Right  x1,y1
            cv2.line(img, (x1, y1), (x1 - lx, y1), color_line, thickness_virtual)
            cv2.line(img, (x1, y1), (x1, y1 - ly), color_line, thickness_virtual)
            if text:
                cv2.putText(img, text, (x, y +15), cv2.FONT_HERSHEY_PLAIN, 2, color_text, thickness)
            return img