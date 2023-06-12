use num_traits::Float;
use std::mem::MaybeUninit;
use std::ops::{
    Add, AddAssign, BitAnd, BitAndAssign, BitOr, BitOrAssign, BitXor, BitXorAssign, Div, DivAssign,
    Index, IndexMut, Mul, MulAssign, Neg, Not, Rem, RemAssign, Shl, ShlAssign, Shr, ShrAssign, Sub,
    SubAssign,
};

#[repr(C)]
#[derive(Copy, Clone)]
pub struct MX<T, const R: usize, const C: usize>
where
    [(); R * C]:,
{
    pub data: [T; R * C],
}

pub type VC<T, const D: usize> = MX<T, D, 1>;
pub type VR<T, const D: usize> = MX<T, 1, D>;

// init

macro_rules! count {
    () => { 0 };
    ($head:expr, $($tail:expr,)*) => { 1 + count!($($tail,)*) };
}

#[macro_export]
macro_rules! matrix {

    (($r:expr, $c:expr) <$t:ty>) => { crate::math::MX::<$t, $r, $c> {
        data: unsafe { MaybeUninit::uninit().assume_init() } }
    };

    (($r:expr, $c:expr) ($v:expr)) => {
        crate::math::MX::<_, $r, $c> { data: [$v; $r * $c] }
    };

    (($r:expr, $c:expr) [$($v:expr)+]) => {
        crate::math::MX::<_, $r, $c> { data: [$($v),+] }
    };

    ($([$($v:expr)+])+) => {(||{
        const R: usize = count!($([$($v),+],)+);
        const C: usize = count!($($($v,)+)+) / R;
        crate::math::MX::<_, R, C> { data: [$($($v,)+)+] }
    })()};

    (VR [$($v:expr)+]) => { (||{
        const R: usize = count!($($v,)+);
        crate::math::VR::<_, R> { data: [$($v,)+] }
    })()};

    (VC [$($v:expr)+]) => { (||{
        const C: usize = count!($($v,)+);
        crate::math::VC::<_, C> { data: [$($v,)+] }
    })()};
}

// iter

impl<T: Copy + Default, const R: usize, const C: usize> FromIterator<T> for MX<T, R, C>
where
    [(); R * C]:,
{
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> Self {
        let mut res = matrix!((R, C)(T::default()));
        iter.into_iter()
            .enumerate()
            .take(R * C)
            .for_each(|(i, v)| res.data[i] = v);
        res
    }
}

impl<T: Copy + Default, const R: usize, const C: usize> IntoIterator for MX<T, R, C>
where
    [(); R * C]:,
{
    type Item = T;
    type IntoIter = std::array::IntoIter<Self::Item, { R * C }>;
    fn into_iter(self) -> Self::IntoIter {
        self.data.into_iter()
    }
}

// index

macro_rules! op_index {
    ($indexer:ty, $prop:ident, $accessor:expr) => {
        impl<T, const R: usize, const C: usize> Index<$indexer> for MX<T, R, C>
        where
            [(); R * C]:,
        {
            type Output = T;
            fn index(&self, $prop: $indexer) -> &Self::Output {
                &self.data[$accessor]
            }
        }

        impl<T, const R: usize, const C: usize> IndexMut<$indexer> for MX<T, R, C>
        where
            [(); R * C]:,
        {
            fn index_mut(&mut self, $prop: $indexer) -> &mut Self::Output {
                &mut self.data[$accessor]
            }
        }
    };
}

op_index!(usize, index, index);
op_index!((usize, usize), index, R * index.0 + index.1);

// operators

macro_rules! op_math_binary {
    ($op:ident::$fn:ident) => {
        impl<T: Copy + Default + $op<Output = T>, const R: usize, const C: usize> $op
            for MX<T, R, C>
        where
            [(); R * C]:,
        {
            type Output = MX<T, R, C>;
            fn $fn(self, rhs: Self) -> Self::Output {
                Self::Output::from_iter(
                    self.data
                        .into_iter()
                        .zip(rhs.data.into_iter())
                        .map(|(a, b)| $op::$fn(a, b)),
                )
            }
        }
        impl<T: Copy + Default + $op<Output = T>, const R: usize, const C: usize> $op<T>
            for MX<T, R, C>
        where
            [(); R * C]:,
        {
            type Output = MX<T, R, C>;
            fn $fn(self, rhs: T) -> Self::Output {
                Self::Output::from_iter(self.data.into_iter().map(|a| $op::$fn(a, rhs)))
            }
        }
    };
}

op_math_binary!(Add::add);
op_math_binary!(Sub::sub);
op_math_binary!(Mul::mul);
op_math_binary!(Div::div);
op_math_binary!(Rem::rem);
op_math_binary!(BitAnd::bitand);
op_math_binary!(BitOr::bitor);
op_math_binary!(BitXor::bitxor);
op_math_binary!(Shl::shl);
op_math_binary!(Shr::shr);

macro_rules! op_math_unary {
    ($op:ident::$fn:ident) => {
        impl<T: Copy + Default + $op<Output = T>, const R: usize, const C: usize> $op
            for MX<T, R, C>
        where
            [(); R * C]:,
        {
            type Output = MX<T, R, C>;
            fn $fn(self) -> Self::Output {
                Self::Output::from_iter(self.data.into_iter().map(|a| $op::$fn(a)))
            }
        }
    };
}

op_math_unary!(Neg::neg);
op_math_unary!(Not::not);

macro_rules! op_math_assign {
    ($op:ident::$fn:ident) => {
        impl<T: Copy + Default + $op, const R: usize, const C: usize> $op for MX<T, R, C>
        where
            [(); R * C]:,
        {
            fn $fn(&mut self, rhs: Self) {
                self.data
                    .iter_mut()
                    .zip(rhs)
                    .for_each(|(a, b)| $op::$fn(a, b));
            }
        }
        impl<T: Copy + Default + $op, const R: usize, const C: usize> $op<T> for MX<T, R, C>
        where
            [(); R * C]:,
        {
            fn $fn(&mut self, rhs: T) {
                self.data.iter_mut().for_each(|a| $op::$fn(a, rhs));
            }
        }
    };
}

op_math_assign!(AddAssign::add_assign);
op_math_assign!(SubAssign::sub_assign);
op_math_assign!(MulAssign::mul_assign);
op_math_assign!(DivAssign::div_assign);
op_math_assign!(RemAssign::rem_assign);
op_math_assign!(BitAndAssign::bitand_assign);
op_math_assign!(BitOrAssign::bitor_assign);
op_math_assign!(BitXorAssign::bitxor_assign);
op_math_assign!(ShlAssign::shl_assign);
op_math_assign!(ShrAssign::shr_assign);

// compare

impl<T: PartialEq, const R: usize, const C: usize> PartialEq for MX<T, R, C>
where
    [(); R * C]:,
{
    fn eq(&self, other: &Self) -> bool {
        self.data.iter().zip(other.data.iter()).all(|(a, b)| a == b)
    }
}

// algebra

impl<T: Float, const R: usize, const C: usize> MX<T, R, C>
where
    [(); R * C]:,
{
    /// Return the matrix dimensions.
    pub fn shape(&self) -> (usize, usize) {
        (R, C)
    }

    /// Return the matrix with changed dimensions, the old and new dimensions must be compatible.
    pub fn reshape<const R_: usize, const C_: usize>(self) -> MX<T, R_, C_>
    where
        [(); (R * C - R_ * C_) * (R_ * C_ - R * C)]:,
    {
        unsafe { *(&self as *const MX<T, R, C> as *const MX<T, R_, C_>) }
    }

    /// Create a new transposed matrix.
    pub fn transpose(&self) -> MX<T, C, R>
    where
        [(); C * R]:,
    {
        let mut res = matrix!((C, R)<T>);
        for i in 0..R {
            for j in 0..C {
                res[R * j + i] = self[C * i + j]
            }
        }
        res
    }

    /// Multiply two matrices.
    pub fn multiply<const C_: usize>(&self, rhs: &MX<T, C, C_>) -> MX<T, R, C_>
    where
        [(); C * C_]:,
        [(); R * C_]:,
    {
        let mut res = matrix!((R, C_)(T::zero()));
        for i in 0..R {
            for j in 0..C_ {
                for k in 0..C {
                    res[C_ * i + j] = res[C_ * i + j] + self[C * i + k] * rhs[C_ * k + j];
                }
            }
        }
        res
    }
}

mod test {

    #[test]
    fn init() {
        let m = matrix!((2, 2)<usize>);
        let m = matrix!((2, 2)(0));
        assert!((0..4).all(|i| m.data[i] == 0));
        let m = matrix!((2,2) [0 1 2 3]);
        assert!((0..4).all(|i| m.data[i] == i));
        let m = matrix!([0 1][2 3]);
        assert!((0..4).all(|i| m.data[i] == i));
        let m: crate::math::VR<usize, 4> = matrix!(VR[0 1 2 3]);
        assert!((0..4).all(|i| m.data[i] == i));
        let m: crate::math::VC<usize, 4> = matrix!(VC[0 1 2 3]);
        assert!((0..4).all(|i| m.data[i] == i));
    }

    #[test]
    fn iter() {
        let m = matrix!([0 1 2 3][4 5 6 7]);
        let ma = crate::math::MX::<i32, 2, 4>::from_iter(m.into_iter());
        let mb = crate::math::MX::<i32, 4, 2>::from_iter(m.into_iter());
        assert!((0..m.data.len()).all(|i| m.data[i] == ma.data[i] && m.data[i] == mb.data[i]));
        let mc = crate::math::MX::<i32, 1, 1>::from_iter(ma.into_iter());
        assert!((0..mc.data.len()).all(|i| mc.data[i] == m.data[i]));
        let md = crate::math::MX::<i32, 2, 2>::from_iter(ma.into_iter());
        assert!((0..md.data.len()).all(|i| md.data[i] == m.data[i]));
    }

    #[test]
    fn index() {
        let mut m = matrix!([0 1 2 3][4 5 6 7]);
        assert!((0..m.data.len()).all(|i| m[i] == i));
        (0..m.data.len()).for_each(|i| m[i] = m[i] * 2);
        assert!((0..m.data.len()).all(|i| m[i] == i * 2));
    }

    #[test]
    fn algebra_mx() {
        let m = matrix!([0.0 1.0 2.0 3.0][4.0 5.0 6.0 7.0]);
        let r = m.reshape::<4, 2>();
        assert!((0..r.data.len()).all(|i| r[i] == m[i]));

        let m = matrix!([0.0 1.0 2.0 3.0][4.0 5.0 6.0 7.0]);
        let m = matrix!([0.0 1.0][4.0 5.0]);
        let r = m.transpose();

        let ma = matrix!([0.0 1.0 2.0 3.0][4.0 5.0 6.0 7.0]);
        let mb = matrix!([0.0 1.0][2.0 3.0][4.0 5.0][6.0 7.0]);
        let r = ma.multiply(&mb);
        assert!(r == matrix!([28.0 34.0][76.0 98.0]));
        assert_eq!(ma.shape(), (2, 4));
        assert_eq!(mb.shape(), (4, 2));
        assert_eq!(r.shape(), (ma.shape().0, mb.shape().1));
    }
}