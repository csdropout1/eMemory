public class hw5 {
    public static void main(String[] args) {
        //2
        System.out.println(isValidPassword("Tr7s6d_"));
        System.out.println(isValidPassword("@abc2-bc"));
        System.out.println(isValidPassword("ALphaa%"));

        //3
        System.out.println(isValidEmail("user_123@gmail.com"));
        System.out.println(isValidEmail("user123alpha@gmail.com"));

        //4
        System.out.println(extractTitle("<item><title>Split (2017)</title><meta><imdb>6375308</imdb></meta>"));


        //5
        System.out.println(sumOfIntegerDiv(new int[]{2, 4, 6, 0, 8, 16}, 4));
        System.out.println(sumOfIntegerDiv(new int[]{2, 4, 6, 0, 8, 16}, 5));


        //6
        System.out.println(swearFilter("A duck was sailing on a ship shipping whole wheat bread. Duck that SHIP!!!",
                new String[]{"duck","ship","whole"}));
    }

        //2
    public static boolean isValidPassword(String s) {
        boolean result = s.matches("[A-Z][\\w]{5,7}");
        if(s.matches("[\\*\\.%]$")) return result = false;
        for (int i = 0; i < s.length(); i++) {
            if ((""+s.charAt(i)).matches("[\\s]")) return result = false;
        }
        return result;
    }

        //3
    public static boolean isValidEmail(String s) {
        boolean result = s.matches("[A-Za-z][\\w]{1,9}[@]{1}[A-Za-z][A-Za-z0-9]{1,11}\\.[a-z]{3}");
        return result;
    }

        //4
    public static String extractTitle(String s) {
        String result = "";
        int start = 0;
        int end = 0;
        for (int i = 0; i< s.length(); i++) {
            if ((s.substring(i, s.length() - 1)).matches("(<title>).+") == true) {
                start = i + 7;
            }
        }
        for (int i = s.length(); i > 0; i--) {
            if ((s.substring(0,i)).matches(".+(</title>)$") == true) {
                end = i - 8;
            }
        }
        result = s.substring(start,end);
        return result;
    }

        //5
    public static int sumOfIntegerDiv(int[] a, int n) {
        int result = 0;
        for (int i = 1; i < n; i++) {
            try {
                result += a[i] / a[i - 1];
            } catch(ArithmeticException e){
                System.out.println("Cannot divide by zero. Skipping index: " + i);
                n++;
            } catch(ArrayIndexOutOfBoundsException e){
                System.out.println("Cannot access array at index: " + i);
                return result;
            } catch(Exception e){
                System.out.print("Something went wring! Skipping index: " + i);
            }
        }
        return result;
    }

        //6
    public static String swearFilter(String text, String[] swear) {
        String texttemp = text.toLowerCase();
        String result = texttemp;
        String[] cursed = new String[swear.length];
        String temp = "";
        for (int i = 0; i < swear.length; i++) {
            temp = "";
            for (int k = 0; k < swear[i].length() - 2; k++) {
                cursed[i] = temp += "*";
            }
            result = result.replaceAll(swear[i], (swear[i].charAt(0)) + cursed[i] + swear[i].charAt(swear[i].length() - 1));
        }
        String finalresult = "";
        for (int i = 0; i <text.length(); i++) {
            if (text.charAt(i) == result.charAt(i)) {
                finalresult += text.charAt(i);
            } else if (result.charAt(i) == '*') {
                finalresult += "*";
            } else {
                finalresult += text.charAt(i);
            }
        }
        return finalresult;
    }
}